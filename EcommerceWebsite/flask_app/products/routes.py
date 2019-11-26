from flask import render_template, url_for, redirect, request, current_app, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import create_app, db

products = Blueprint('products', __name__)