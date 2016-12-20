from app import db
from sqlalchemy import func
MAP = {
    "基础知识": "basic",
    "机器学习": "machine-learning",
    "网站开发": "web-development",
    "数据挖掘": "data-mining",
    "第三方库": "3rd-library",
    "图像处理": "image-processing",
    "工具资源": "tools-n-resources",
    "爬虫技术": "spider-man",
}
class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column('issue_id', db.Integer, primary_key=True, autoincrement=True)
    html_id = db.Column(db.Integer)
    title = db.Column(db.String(250))
    url = db.Column(db.String(255))
    excerpt = db.Column(db.Text)
    face = db.Column(db.String(255))
    col_date = db.Column(db.DateTime, default=func.now())
    pub_date = db.Column(db.DateTime)

    comment = db.Column(db.Text)
    comment_auther = db.Column(db.String(32))
    comment_auther_id = db.Column(db.String(32), doc="GitHub ID")

    views = db.Column(db.Integer, server_default='1')
    votes = db.Column(db.Integer, server_default='1')
    share = db.Column(db.Integer, server_default='0')

    is_public = db.Column(db.Boolean, server_default='0')
    topic_name = db.Column(db.String(64), nullable=False)
    topic_slug = db.Column(db.String(64), nullable=False)
    def __init__(self, title, html_id, excerpt, url, src):
        self.title = title
        self.html_id = html_id
        self.url = url
        self.face = src
        self.excerpt = excerpt

class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column("topic_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(64), unique=True, index=True)

    views = db.Column(db.Integer, server_default='1', nullable=True)
    issues = db.Column(db.Integer, server_default='0')
    followers = db.Column(db.Integer, server_default='1')
    rank = db.Column(db.Integer)

    def __init__(self, name, slug, rank=1):
        self.name = name
        self.slug = slug
        self.rank = rank

def init_topic():
    for name, slug in MAP.items():
        topic = Topic(name, slug)
        db.session.add(topic)
        db.session.commit()

