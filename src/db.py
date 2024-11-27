from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

User_Rates = db.Table(
                    "student_rates", db.Model.metadata,
                    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                    db.Column("rate_id", db.Integer, db.ForeignKey("rates.id"))
                    )

Group_Rates = db.Table(
                    "group_rates", db.Model.metadata,
                    db.Column("group_id", db.Integer, db.ForeignKey("groups.id")),
                    db.Column("rate_id", db.Integer, db.ForeignKey("rates.id"))
                    )

    
class Group(db.Model):
    """
    Group Model
    """

    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User", cascade="delete")
    tasks = db.relationship("Task", cascade="delete")
    rates = db.relationship("Rate", secondary=Group_Rates, back_populates="groups")

    def __init__(self, **kwargs):
        """
        Initializes group object/entry
        """
        self.name= kwargs.get("name")
   
    def serialize(self):
        """
        Serializes a group object
        """
    
        return {
            "id": self.id,
            "name": self.name,
            "users": [u.serialize() for u in self.users],
            "tasks": [t.serialize() for t in self.tasks],
            "rates": [r.serialize() for r in self.rates]
               }

    def simple_serialize(self):
        """
        Simple serializes a group object
        """

        return {
                "id": self.id,
                "name": self.name
                }


class User(db.Model):
    """
    User Model 
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    rates = db.relationship("Rate", secondary=User_Rates, back_populates="users")

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
                "rates": [r.serialize() for r in self.rates]
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


class Rate(db.Model):
    """
    Rate Model
    """

    __tablename__ = "rates"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stars = db.Column(db.Integer, nullable=False)
    users = db.relationship("User", secondary=User_Rates, back_populates='rates')
    groups = db.relationship("Group", secondary=Group_Rates, back_populates='rates')


    def __init__(self, **kwargs):
        """
        Initializes an rate object
        """

        self.stars = kwargs.get("stars")

    def serialize(self):
        """
        Serializes rate object
        """

        return {
                "id": self.id,
                "stars": self.stars,
                }

    def simple_serialize(self):
        """
        Simple Serializes a rate object
        """

        return {
                "id": self.id,
                "stars": self.stars,
                }


class Task(db.Model):
    """
    Task Model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
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
                "task_name": self.name,
                "task_description": self.description,
                "due_date": self.due_date
                }