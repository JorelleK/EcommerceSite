from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import os


csp = {
    'default-src': [
        '\'self\'',
        'https://code.jquery.com/',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/',
        'https://stackpath.bootstrapcdn.com/bootstrap/'
    ]
}



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flask_app.admin.routes import admin
    from flask_app.main.routes import main
    from flask_app.users.routes import users
    from flask_app.products.routes import products

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(products)
    app.register_blueprint(users)

    return app

