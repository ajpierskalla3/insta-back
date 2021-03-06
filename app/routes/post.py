from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.posts import Post
from ..models.users import User
from ..models.follows import Follow
from ..models.likes import Like
from ..models.comments import Comment
from ..auth import require_auth
from random import randint

bp = Blueprint("posts", __name__, url_prefix="/api/post")


@bp.route('/scroll/<length>')
def index(length):
    length = int(length)
    post_list = []
    post_num = Post.query.count()
    posts = []
    rand_int = randint(1, post_num-3)
    posts = Post.query.filter(Post.id > rand_int).limit(3).all()
    for post in posts:
        post_dict = post.to_dict()
        likes = Like.query.filter(
            Like.likeable_id == post_dict["id"] and Like.likeableType == 'post').count()
        comments = Comment.query.filter(
            Comment.post_id == post_dict["id"]).count()
        post_dict["like_count"] = likes
        post_dict["comment_count"] = comments
        post_list.append(post_dict)
    return {"posts": post_list}


@bp.route('/<id>/scroll/<length>')
def home_feed(id, length):
    length = int(length)
    post_list = []
    followed_users = Follow.query.filter(Follow.user_id == id).all()
    for followed in followed_users:
        posts = Post.query.filter(Post.user_id == followed.user_followed_id).slice(length, length + 3)
        print(len(list(posts)))
        found_users = {}
        for post in posts:
            post_dict = post.to_dict()
            if post.user_id in found_users:
                post_dict["user_info"] = found_users[post.user_id]
            else:
                user = post.user
                found_users[post.user_id] = {"username": user.username, "profilePic": user.profile_image_url}
                post_dict["user_info"] = found_users[post.user_id]

            likes = Like.query.filter(Like.likeable_id == post.id).filter(Like.likeable_type == 'post').all()
            post_dict['likeCount'] = len(likes)
            likes_list = []
            for like in likes:
                likes_list.append(like.user.to_dict())
            post_dict['likesList'] = likes_list

            comments = post.comments
            original_comments = comments
            if len(comments) > 2:
                comments = comments[-2:]
            comments_list = []
            for comment in comments:
                comment_dict = comment.to_dict()
                comment_likes = Like.query.filter(Like.likeable_type == "comment").filter(Like.likeable_id == comment.id).all()
                user_list = []
                for like in comment_likes:
                    username = like.user.to_dict()
                    user_list.append(username)

                comment_dict['likes_comment'] = user_list

                if comment.user_id in found_users:
                    comment_dict["username"] = found_users[comment.user_id]
                else:
                    user = comment.user
                    found_users[user.id] = {"username": user.username, "profilePic": user.profile_image_url}
                    comment_dict["username"] = found_users[comment.user_id]

                comments_list.append(comment_dict)

            post_dict["comments"] = {"total": len(original_comments), "commentsList": comments_list }

            post_list.append(post_dict)
            if len(post_list) == 3:
                return {"posts": post_list}
    return {"posts": post_list}


@bp.route('/<post_id>')
def get_post(post_id):

    post = Post.query.filter(Post.id == post_id).first()
    post_dict = post.to_dict()
    post_dict["user"] = post.user.to_dict()
    comments = post.comments
    comments_list = []

    for comment in comments:
        comment_dict = comment.to_dict()

        comment_likes = Like.query.filter(Like.likeable_type == "comment").filter(Like.likeable_id == comment.id).all()
        user_list = []
        for like in comment_likes:
            user = like.user.to_dict()
            user_list.append(user)

        comment_dict['likes_comment'] = user_list

        user = comment.user
        comment_dict["username"] = user.to_dict()
        comments_list.append(comment_dict)

    likes = Like.query.filter(Like.likeable_type == "post").filter(Like.likeable_id == post_id).all()
    user_list = []

    for like in likes:
        user = like.user.to_dict()
        user_list.append(user)


    return {"post": post_dict, "comments": comments_list, "likes_post": user_list}
