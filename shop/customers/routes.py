from flask import render_template, session, redirect, request, url_for, flash, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from shop import db, bcrypt
from shop.customers.forms import RegistrationForm, LoginForm, UpdateForm
from shop.customers.models import Customer
customers = Blueprint('customers', __name__)


@customers.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        customer = Customer(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(customer)
        db.session.commit()

        return redirect(url_for('customers.loginpage'))

    return render_template('customers/register.html', title='Registration Page', form=form)


@customers.route("/loginpage", methods=['GET', 'POST'])
def loginpage():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(username=form.username.data).first()

        if customer is not None and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            flash(f'Welcome {form.username.data} You are logged-in now', 'success')
            return redirect(url_for('customers.account'))
        else:
            flash('Wrong Username/Password please try again', 'danger')

    return render_template('customers/login.html', title='Customer Login Page', form=form)


@customers.route("/logout")
def logout():
    username = current_user.username
    logout_user()
    current_app.logger.info('%s logged out successfully', username)
    return redirect(url_for('main.home'))


@customers.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()

        return redirect(url_for('customers.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('customers/account.html', title='Account', form=form)