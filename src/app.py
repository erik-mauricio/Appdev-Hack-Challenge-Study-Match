import json
import os
from db import db
from flask import Flask, request
from db import Group, User, Rate, Task, Post, Comment

app = Flask(__name__)
db_filename = "StudentMatch.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# Routes

# User routes: Create user, get all users, get specific user by user id and delete specific user by user id


@app.route("/users/", methods=["POST"])
def create_user():
    """
    Endpoint to create a user
    """

    body = json.loads(request.data)
    if "name" not in body:
        return failure_response("User name is required", 400)
    if "netid" not in body:
        return failure_response("User netid is required", 400)
    user = User(name=body["name"], netid=body["netid"])
    db.session.add(user)
    db.session.commit()
    return success_response(user.simple_serialize(), 201)


@app.route("/users/<int:user_id>/", methods=["PUT"])
def assign_user_to_group(user_id):
    """
    Endpoint to assign a user to a group
    """

    body = json.loads(request.data)
    if "group_id" not in body:
        return failure_response("Group id is required", 400)
    group = Group.query.filter_by(id=body["group_id"]).first()
    if group is None:
        return failure_response("Group not found", 404)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 404)
    user.group_id = body["group_id"]
    group.users.append(user)
    db.session.commit()
    return success_response(group.serialize(), 200)


@app.route("/users/", methods=["GET"])
def get_users():
    """
    Endpoint to get all users
    """

    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users}, 200)


@app.route("/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint to get all user by id
    """

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 404)
    return success_response(user.serialize(), 200)


@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint to get delete user by id
    """

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found", 404)
    group = Group.query.filter_by(id=user.group_id).first()
    if group is not None:
        group.users.remove(user)
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize(), 200)


# Group Routes: Create group, get all groups, get specific group by group id and delete specific group by group id


@app.route("/groups/", methods=["POST"])
def create_group():
    """
    Endpoint to get create group
    """

    body = json.loads(request.data)
    if "name" not in body:
        return failure_response("Group name is required", 400)
    group = Group(name=body["name"])
    db.session.add(group)
    db.session.commit()
    return success_response(group.serialize(), 201)


@app.route("/groups/", methods=["GET"])
def get_groups():
    """
    Endpoint to get all groups
    """

    groups = [group.serialize() for group in Group.query.all()]
    return success_response({"groups": groups}, 200)


@app.route("/groups/<int:group_id>/", methods=["GET"])
def get_group(group_id):
    """
    Endpoint to get all a group by id
    """

    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found", 404)
    return success_response(group.serialize(), 200)


@app.route("/groups/<int:group_id>/", methods=["DELETE"])
def delete_group(group_id):
    """
    Endpoint to delete a group by id
    """

    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found", 404)
    db.session.delete(group)
    db.session.commit()
    return success_response(group.serialize(), 200)


# Task routes: Create task for particular group id, update task for particular task id, get all tasks, get all tasks for a particular group, get specific task by task id, and delete specific task by task id


@app.route("/groups/<int:group_id>/tasks/", methods=["POST"])
def create_task(group_id):
    """
    Endpoint to create a task
    """

    body = json.loads(request.data)
    if "task_name" not in body:
        return failure_response("Task name is required", 400)
    if "description" not in body:
        return failure_response("Task description is required", 400)
    if "due_date" not in body:
        return failure_response("Task due date is required", 400)
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found", 404)
    task = Task(
        task_name=body["task_name"],
        description=body["description"],
        due_date=body["due_date"],
        comments=group_id,
    )
    group.tasks.append(task)
    db.session.add(task)
    db.session.commit()
    return success_response(group.serialize(), 201)


@app.route("/tasks/<int:task_id>/", methods=["PUT"])
def update_task(task_id):
    """
    Endpoint to update a task
    """

    body = json.loads(request.data)
    if "task_name" not in body and "description" not in body and "due_date" not in body:
        return failure_response(
            "Atleast one amongst task name, description, or due date is required", 400
        )
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found", 404)
    group = Group.query.filter_by(id=task.comments).first()
    group.tasks.remove(task)
    if "task_name" in body:
        task.task_name = body["task_name"]
    if "description" in body:
        task.description = body["description"]
    if "due_date" in body:
        task.due_date = body["due_date"]
    group.tasks.append(task)
    db.session.commit()
    return success_response(group.serialize(), 200)


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    """
    Endpoint to get all tasks
    """

    tasks = [task.serialize() for task in Task.query.all()]
    return success_response({"tasks": tasks}, 200)


@app.route("/tasks/<int:task_id>/", methods=["GET"])
def get_specific_task(task_id):
    """
    Endpoint to get all task by specific id
    """

    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found", 404)
    return success_response(task.serialize(), 200)


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_specific_task(task_id):
    """
    Endpoint to delete all task by specific id
    """

    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("Task not found", 404)
    group = Group.query.filter_by(id=task.comments).first()
    group.tasks.remove(task)
    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize(), 200)


# Post Routes: Create post, get all posts, get specific post by post id and delete specific post by post id


@app.route("/posts/", methods=["POST"])
def create_post():
    """
    Endpoint to create post
    """
    
    body = json.loads(request.data)
    if "post_name" not in body:
        return failure_response("Post name is required", 400)
    if "description" not in body:
        return failure_response("Post description is required", 400)
    if "timestamp" not in body:
        return failure_response("Post timestamp is required", 400)
    post = Post(
        post_name=body["post_name"],
        description=body["description"],
        timestamp=body["timestamp"],
    )
    db.session.add(post)
    db.session.commit()
    return success_response(post.serialize(), 201)


@app.route("/posts/", methods=["GET"])
def get_posts():
    """
    Endpoint to get all posts
    """
    posts = [post.serialize() for post in Post.query.all()]
    return success_response({"posts": posts}, 200)


@app.route("/posts/<int:post_id>/", methods=["GET"])
def get_post(post_id):
    """
    Endpoint to get post 
    """

    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found", 404)
    return success_response(post.serialize(), 200)


@app.route("/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    """
    Endpoint to delete post by id
    """

    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found", 404)
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize(), 200)


# Comments routes: Create comment for particular post id, update comment for particular comment id, get all tasks, get specific comment by comment id, and delete specific comment by comment id


@app.route("/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    """
    Endpoint to create comment
    """

    body = json.loads(request.data)
    if "description" not in body:
        return failure_response("Comment description is required", 400)
    if "timestamp" not in body:
        return failure_response("Comment timestamp is required", 400)
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found", 404)
    comment = Comment(
        description=body["description"], timestamp=body["timestamp"], post_id=post_id
    )
    post.comments.append(comment)
    db.session.add(comment)
    db.session.commit()
    return success_response(post.serialize(), 201)


@app.route("/comments/<int:comment_id>/", methods=["PUT"])
def update_comment(comment_id):
    """
    Endpoint to update comment
    """

    body = json.loads(request.data)
    if "description" not in body:
        return failure_response("Comment description is required", 400)
    if "timestamp" not in body:
        return failure_response("Comment timestamp is required", 400)
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found", 404)
    post = Post.query.filter_by(id=comment.post_id).first()
    post.comments.remove(comment)
    comment.description = body["description"]
    comment.timestamp = body["timestamp"]
    post.comments.append(comment)
    db.session.commit()
    return success_response(post.serialize(), 200)


@app.route("/comments/", methods=["GET"])
def get_all_comments():
    """
    Endpoint to get all comments
    """

    comments = [comment.serialize_with_post() for comment in Comment.query.all()]
    return success_response({"comments": comments}, 200)


@app.route("/comments/<int:comment_id>/", methods=["GET"])
def get_specific_comment(comment_id):
    """
    Endpoint to get all comment by id
    """

    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found", 404)
    return success_response(comment.serialize_with_post(), 200)


@app.route("/comments/<int:comment_id>/", methods=["DELETE"])
def delete_specific_comment(comment_id):
    """
    Endpoint to delete comment by id
    """

    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found", 404)
    post = Post.query.filter_by(id=comment.post_id).first()
    post.comments.remove(comment)
    db.session.delete(comment)
    db.session.commit()
    return success_response(comment.serialize_with_post(), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
