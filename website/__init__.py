from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import db

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'

    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)

    # Import models within the create_app function to avoid circular imports
    from .models import Todo, Category

    from .views import my_view
    app.register_blueprint(my_view)

    with app.app_context():
        db.create_all()
        from .views import add_common_categories
        add_common_categories()

    return app


