from flask import Flask, render_template, request, json, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import hmac, hashlib
import html, re

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

GITHUB_SEC = os.environ.get('GITHUB_WH_SEC')

from models import Topic, Issue, MAP
SLUGS = [MAP[k] for k in MAP]

@app.route('/')
def hello_world():
    return render_template("index.html", topics = Topic.query.all())

@app.route('/t')
@app.route('/t/<topic>')
def topic_homepage(topic='all'):
    if topic not in SLUGS:
        return redirect("/")
    topic_info = Topic.query.filter_by(slug=topic).first()
    issues = Issue.query.filter_by(topic_slug=topic).limit(20)
    return render_template("topic.html", topic = topic_info, issues = issues)

@app.route('/i/<issue_id>')
def issue_page(issue_id=''):
    return issue_id

@app.route('/wh/github', methods=['POST'])
def webhook_github():
    if False and not verify_webhook_signature(request.headers.get('X-Hub-Signature'), request.data):
        return "OFF"
    event = request.headers.get('X-GitHub-Event')
    if "push" == event:
        os.system("git pull")
        return "Pulled"

    payload = json.loads(request.data.decode())
    action = payload.get("action")
    if "issues" == event:
        # action: opened, reopened
        if verify_webhook_author(payload):
            return make_response("You're not authorized", 403)
        if "opened" == action or "reopened" == action:
            try:
                i_title = payload.get("issue").get("title")
                i_html_id = payload.get("issue").get("number")
                i_body = html.unescape(payload.get("issue").get("body"))
                i_excerpt = i_body.split('<br>')[1].strip()
                matched = re.findall(r'src="(.*?)"[\s\S]*?via Pocket (.*?)<', i_body)
                new_issue = Issue(i_title, i_html_id, i_excerpt, matched[0][1], matched[0][0])
                db.session.add(new_issue)
                db.session.commit()
            except KeyError:
                return make_response("KeyError", 500)
        elif "labeled" == action:
            i_html_id = payload.get("issue").get("number")
            issue = Issue.query.filter_by(html_id=i_html_id).first()
            if not issue:
                return make_response("No such issue {}".format(i_html_id), 500)
            labels = payload.get("issue").get("labels")
            for label in labels:
                lname = label.get("name")
                if lname == "cmd::PUB":
                    issue.is_public = True
                elif lname in MAP:
                    # first label only
                    issue.topic_name = lname
                    issue.topic_slug = MAP.get(lname)
                    t = Topic.query.filter_by(slug=MAP.get(lname)).first()
                    t.issues += 1

            db.session.commit()
        elif "unlabeled" == action:
            pass

    elif "issue_comment" == event:
        # action: "created", "edited", or "deleted"
        pass
    return "Event received!"

def verify_webhook_signature(sig, payload):
    sha_name, signature = sig.split("=")
    if sha_name != "sha1":
        return False
    mac = hmac.new(GITHUB_SEC.encode(), msg=payload, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)
def verify_webhook_author(payload):
    return "rainyear" != payload.get("issue").get("user").get("login")
