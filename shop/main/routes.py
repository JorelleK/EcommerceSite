from flask import render_template, Blueprint, request, current_app, redirect, url_for, flash, session
from shop import db, bcrypt
from shop.admin.forms import RegistrationForm, LoginForm
from shop.products.forms import OrderForm
from shop.admin.models import User
from shop.products.models import Addproduct
from flask_login import login_user
import os
import json

main = Blueprint('main', __name__)

@main.route("/admin")
def admin():
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@main.route("/")
def home():
    form = OrderForm(request.form)
    # products = Addproduct.query.all()

    tshirt = Addproduct.query.filter_by(desc='T-Shirt').all()
    jewelry = Addproduct.query.filter_by(desc='Jewelry').all()
    sunglasses = Addproduct.query.filter_by(desc='Sunglasses').all()
    bands = Addproduct.query.filter_by(desc='Bands').all()

    return render_template('home.html', tshirt=tshirt, jewelry=jewelry, sunglasses=sunglasses, bands=bands, form=form)


@main.route("/about")
def about():

    return render_template('about.html', title='About')


@main.route("/csp_error_handling", methods=["POST"])
def report_handler():
    """
    Receives POST requests from the browser whenever the Content-Security-Policy
    is violated. Processes the data and logs an easy-to-read version of the message
    in your console.
    """
    report = json.loads(request.data.decode())["csp-report"]

    # current_app.logger.info(json.dumps(report, indent=2))

    violation_desc = "\nViolated directive: %s, \nBlocked: %s, \nOriginal policy: %s \n" % (
        report["violated-directive"],
        report["blocked-uri"],
        report["original-policy"]
    )

    current_app.logger.info(violation_desc)
    return redirect(url_for("main.home"))


# @main.route('/admin')
# def home():
#     if 'username' not in session:
#         flash('Please login first', 'danger')
#         return redirect(url_for('admin.login'))
#       #products = Addproduct.query.all()
#     return render_template('admin/index.html', title='Admin Page')