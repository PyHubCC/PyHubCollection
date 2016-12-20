from flask import Flask, render_template, request, json, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import hmac, hashlib
import html, re

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

GITHUB_SEC = os.environ.get('GITHUB_WH_SEC')

from models import Topic, Issue

@app.route('/')
def hello_world():
    return render_template("index.html", topics = Topic.query.all())

@app.route('/t')
@app.route('/t/<topic>')
def topic_homepage(topic='all'):
    topic_info = Topic.query.filter_by(slug=topic).first()
    issues = Issue.query.filter_by(topic=topic).limit(20)
    return render_template("topic.html", topic = topic_info, issues = issues)

@app.route('/i/<issue_id>')
def issue_page(issue_id=''):
    return issue_id

@app.route('/wh/github', methods=['POST'])
def webhook_github():
    if not verify_webhook_signature(request.headers.get('X-Hub-Signature'), request.data):
        return "OFF"
    event = request.headers.get('X-GitHub-Event')
    if "push" == event:
        os.system("git pull")
        return "Pulled"

    payload = json.loads(request.data.decode())
    action = payload.get("action")
    if "issues" == event:
        # action: opened
        if "rainyear" != payload.get("issue").get("user").get("login"):
            return make_response("You're not authorized", 403)
        if "opened" == action:
            try:
                i_title = payload.get("issue").get("title")
                i_html_id = payload.get("html_url")
                i_body = html.unescape(payload.get("issue").get("body"))
                i_excerpt = i_body.split('<br>')[1].strip()
                matched = re.findall(r'src="(.*?)"[\s\S]*?via Pocket (.*?)<', i_body)
                new_issue = Issue(i_title, i_html_id, i_excerpt, matched[0][1], matched[0][0])
                db.session.add(new_issue)
                db.session.commit()
            except KeyError:
                return make_response("KeyError", 500)

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
