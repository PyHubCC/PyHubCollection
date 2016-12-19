from app import db

class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column('issue_id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(255))
    excerpt = db.Column(db.Text)
    col_date = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)

    comment = db.Column(db.Text)
    comment_auther = db.Column(db.String(32))
    comment_auther_id = db.Column(db.String(32), doc="GitHub ID")

    views = db.Column(db.Integer, server_default='1')
    votes = db.Column(db.Integer, server_default='1')
    share = db.Column(db.Integer, server_default='0')

    is_public = db.Column(db.Boolean, server_default='0')
    topic = db.Column(db.String(64), nullable=False)

class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column("topic_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    slug = db.Column(db.String(64), unique=True, index=True)

    views = db.Column(db.Integer, server_default='1', nullable=True)
    issues = db.Column(db.Integer, server_default='0')
    followers = db.Column(db.Integer, server_default='1')


