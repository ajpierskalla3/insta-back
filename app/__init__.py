from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.config import Configuration

from app.routes import session, comment, profile, follow, like, post, user, notification, search, aws

from app.models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(session.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(follow.bp)
app.register_blueprint(like.bp)
app.register_blueprint(post.bp)
app.register_blueprint(notification.bp)
app.register_blueprint(user.bp)
app.register_blueprint(comment.bp)
app.register_blueprint(search.bp)
app.register_blueprint(aws.bp)
