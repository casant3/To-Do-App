from .database import db


class Todo(db.Model):
    #fill in a column with a number, gives the object a unique id on creation
    id = db.Column(db.Integer, primary_key = True)
    #fill column with string that cant be longer than 300 characters, the task must be unique
    task = db.Column(db.String(300), unique = True)
    complete = db.Column(db.Boolean, default = False)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tasks = db.relationship('Task', backref='category', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    