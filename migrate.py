from app import db
from models import init_topic

db.drop_all()
db.create_all()
init_topic()
