from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import my_view
from .database import db


#use db to edit the database file using dot notation

# new instance of the Flask class
def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.secret_key = 'your_secret_key_here'
    db.init_app(app)
    
    app.register_blueprint(my_view)
    
    from .models import Todo
    with app.app_context():
        db.create_all()
        from .views import add_common_categories
        add_common_categories()
        
    return app