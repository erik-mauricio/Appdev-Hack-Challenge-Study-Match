from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Group(db.Model):
    """
    Group Model
    """

    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User")
    tasks = db.relationship("Task", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initializes group object/entry
        """
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serializes a group object
        """

        return {
            "id": self.id,
            "name": self.name,
            "users": [user.serialize() for user in self.users],
            "tasks": [task.serialize() for task in self.tasks],
        }

    def simple_serialize(self):
        """
        Simple serializes a group object
        """

        return {"id": self.id, "name": self.name}


class User(db.Model):
    """
    User Model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)

    def __init__(self, **kwargs):
        """
        Initializes a user object
        """

        self.name = kwargs.get("name")
        self.netid = kwargs.get("netid")

    def serialize(self):
        """
        Serializes a user object
        """

        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "group_id": self.group_id,
        }

    def simple_serialize(self):
        """
        Simple Serializes a user object
        """

        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
        }


class Task(db.Model):
    """
    Task Model
    """

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    due_date = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes an task object
        """

        self.task_name = kwargs.get("task_name")
        self.description = kwargs.get("description")
        self.due_date = kwargs.get("due_date")

    def serialize(self):
        """
        Serializes task object
        """

        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_description": self.description,
            "due_date": self.due_date,
            "group_id": self.group_id,
        }


class Post(db.Model):
    """
    Post Model
    """

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initializes a post object
        """

        self.post_name = kwargs.get("post_name")
        self.description = kwargs.get("description")
        self.timestamp = kwargs.get("timestamp")

    def serialize(self):
        """
        Serializes post object
        """

        return {
            "id": self.id,
            "post_name": self.post_name,
            "post_description": self.description,
            "timestamp": self.timestamp,
            "comments": [comment.serialize() for comment in self.comments],
        }


class Comment(db.Model):
    """
    Commment Model
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes a comment object
        """

        self.description = kwargs.get("description")
        self.timestamp = kwargs.get("timestamp")

    def serialize(self):
        """
        Serializes a comment object
        """

        return {
            "id": self.id,
            "comment_description": self.description,
            "timestamp": self.timestamp,
        }

    def serialize_with_post(self):
        """
        Serializes a comment object with post id
        """

        return {
            "id": self.id,
            "comment_description": self.description,
            "timestamp": self.timestamp,
            "post_id": self.post_id,
        }
