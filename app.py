from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
import os
import hmac, hashlib

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
    if  event == 'push':
        os.system("git pull")
    return "OK"

def verify_webhook_signature(sig, payload):
    sha_name, signature = sig.split("=")
    if sha_name != "sha1":
        return False
    mac = hmac.new(GITHUB_SEC.encode(), msg=payload, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)
