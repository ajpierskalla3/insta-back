from ..models import db
from sqlalchemy import func


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        nullable=False)
    image_url = db.Column(db.String(2000), nullable=False)
    caption = db.Column(db.String(2000), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now(),
                           nullable=False)

    user = db.relationship("User", back_populates="posts")
    saved = db.relationship("Saved_Post", back_populates="post")
    comments = db.relationship("Comments", back_populates="post")