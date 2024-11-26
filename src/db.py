from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    pass

class User(db.Model):
    pass

class Rate(db.Model):
    pass