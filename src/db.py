from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Rating_To_Student = db.Table(
                    "student_ratings", db.Model.metadata,
                    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
                    )

Rating_To_Group = db.Table(
                    "group_ratings", db.Model.metadata,
                    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"))
                    )

class User(db.Model):
    """
    User Model 
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)

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
                "netid": self.netid
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
    

class Group(db.Model):
    """
    Group Model
    """

    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initializes group object/entry
        """
        self.name= kwargs.get("name")
        self.users = kwargs.get("users")
   
    def serialize(self):
        """
        Serializes a group object
        """
    
        return {
            "id": self.id,
            "name": self.name,
            "users": [u.serialize() for u in self.users]
               }

    def simple_serialize(self):
        """
        Simple serializes a group object
        """

        return {
                "id": self.id,
                "name": self.name
                }

class Rate(db.Model):

    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stars = db.Column(db.Integer, nullable=False)


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