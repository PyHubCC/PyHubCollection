from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
import sys

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

GITHUB_SEC = os.environ.get('GITHUB_WH_SEC')

from models import Topic

@app.route('/')
def hello_world():
    return render_template("index.html", topics = Topic.query.all())

@app.route('/t')
@app.route('/t/<topic>')
def topic_homepage(topic='all'):
    return topic

@app.route('/i/<issue_id>')
def issue_page(issue_id=''):
    return issue_id
@app.route('/wh/github', methods=['POST'])
def webhook_github():
    if request.headers['X-GitHub-Event'] == 'push':
        os.system("git pull")
    print(request.headers)
    print(verify_webhook_signature(request.headers['X-Hub-Signature'], request.data))
    return "OK"

def verify_webhook_signature(sig, payload):
    sha = hashlib.sha1(GITHUB_SEC + payload)

    return sig == 'sha1=' + sha.hexdigest()
