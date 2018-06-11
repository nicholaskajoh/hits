import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from datetime import datetime, timedelta

# load environment variables
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(APP_ROOT, '.env'))

# create Flask app
app = Flask(__name__)

# setup DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

# create model
class Hit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Hit %r>' % self.created_at

# create DB table(s) if non-existent
db.create_all()

# setup Redis
app.config['REDIS_URL'] = os.getenv('REDIS_URL')
redis_store = FlaskRedis(app)

# index view
@app.route("/")
def index():
    # get hits
    if redis_store.get('all_time_hits_count') is not None:
        all_time_hits_count = redis_store.get('all_time_hits_count').decode('utf-8')
    else:
        all_time_hits_count = Hit.query.count()
        redis_store.set('all_time_hits_count', all_time_hits_count, ex=60)

    a_day_ago = datetime.now() - timedelta(hours=24)
    last_day_hits_count = Hit.query.filter(Hit.created_at >= a_day_ago).count()

    # save hit
    new_hit = Hit()
    db.session.add(new_hit)
    db.session.commit()
    
    return render_template(
        'index.html',
        all_time_hits_count=all_time_hits_count,
        last_day_hits_count=last_day_hits_count,
        instance_id=os.getenv('INSTANCE_ID')
    )