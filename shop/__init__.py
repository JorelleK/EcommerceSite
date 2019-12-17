from flask import Flask
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_mail import Mail

import os

csp = {
    'default-src': [
        '\'self\'',
        'https://code.jquery.com/',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/',
        'https://stackpath.bootstrapcdn.com/bootstrap/'
    ]
}

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


talisman = Talisman(content_security_policy=csp)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'customers.loginpage'

mail = Mail()
basedir = os.path.abspath(os.path.dirname(__file__))
photos = UploadSet('photos', IMAGES)


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    configure_uploads(app, photos)
    patch_request_class(app)

    app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = 'cmsctest01@gmail.com'
    app.config["MAIL_PASSWORD"] = 'Iwbahmi2@19'

    talisman.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from shop.admin.routes import admin
    from shop.products.routes import products
    from shop.main.routes import main
    from shop.customers.routes import customers

    app.register_blueprint(admin)
    app.register_blueprint(products)
    app.register_blueprint(main)
    app.register_blueprint(customers)

    with app.app_context():
        db.create_all()

    talisman.content_security_policy = csp
    talisman.content_security_policy_report_uri = "/csp_error_handling"

    return app

