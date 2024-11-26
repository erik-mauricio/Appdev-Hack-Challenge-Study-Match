from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User Model 
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.Integer, nullable=False)

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
    pass

class Rate(db.Model):
    pass