from flask import render_template, Blueprint

from flask_app.models import User

main = Blueprint('main', __name__)