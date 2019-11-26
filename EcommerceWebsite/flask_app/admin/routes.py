from flask import render_template, url_for, redirect, request, current_app, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required


from flask_app import create_app, db, bcrypt
from flask_app.users.forms import RegistrationForm, LoginForm
from flask_app.models import User

admin = Blueprint('admin', __name__)

@admin.route("/")
def index():
    return render_template('index.html', title='Home')

@admin.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.login'))

    return render_template('register.html', title='Register', form=form)

@admin.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('users.account'))

    return render_template('login.html', title='Login', form=form)

@admin.route("/about")
def about():
    return "About page"