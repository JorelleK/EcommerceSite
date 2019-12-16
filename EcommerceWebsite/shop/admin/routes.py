from flask import render_template, session, redirect, request, url_for, flash, Blueprint
from flask_login import login_user
from shop import db, bcrypt
from shop.admin.forms import RegistrationForm, LoginForm
from shop.products.forms import AddProduct
from shop.admin.models import User
from shop.products.models import Addproduct, Brand, Category


import qrcode
import qrcode.image.svg as svg

from io import BytesIO

admin = Blueprint('admin', __name__)


@admin.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        session['reg_username'] = user.username

        return redirect(url_for('admin.tfa'))

    return render_template('admin/register.html', title='Registration Page', form=form)


@admin.route("/tfa")
def tfa():
    if 'reg_username' not in session:
        return redirect(url_for('main.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

    return render_template('admin/tfa.html'), headers

@admin.route("/qr_code")
def qr_code():
    if 'reg_username' not in session:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(username=session['reg_username']).first()

    session.pop('reg_username')

    img = qrcode.make(user.get_auth_uri(), image_factory=svg.SvgPathImage)

    stream = BytesIO()

    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'  # Expire immediately, so browser has to reverify everytime
    }

    return stream.getvalue(), headers


@admin.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate():  # form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            login_user(user)
            flash(f'Welcome {form.username.data} You are logged-in now', 'success')
            return redirect(request.args.get('next') or url_for('main.admin'))
        else:
            flash('Wrong Username/Password please try again', 'danger')

    return render_template('admin/login.html', title='Login Page', form=form)


@admin.route("/brands", methods=['GET', 'POST'])
def brands():
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    form = AddProduct()
    return render_template("admin/brand.html", title="Brand Page", brands=brands, form=form)


@admin.route("/category")
def category():
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template("admin/brand.html", title="Category Page", categories=categories)



