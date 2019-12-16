from datetime import datetime

from flask import redirect, render_template, url_for, flash, request, Blueprint, session, current_app
from shop import db, photos
from shop.products.forms import AddBrandForm, AddCatForm, AddProduct, OrderForm
from shop.products.models import Brand, Category, Addproduct, Order
import secrets, os

products = Blueprint('products', __name__)


@products.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))

    form = AddBrandForm()

    if request.method == 'POST':
        getbrand = form.name.data
        brand = Brand(name=getbrand)

        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your databse', 'success')
        db.session.commit()
        return redirect(url_for('products.addbrand'))

    return render_template('products/addbrand.html', brands='brands', form=form)


@products.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):

    if 'username' not in session:
        flash('Please login first', 'danger')

    form = AddBrandForm()
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')

    if request.method == 'POST':
        updatebrand.name = brand
        flash('Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('admin.brands'))

    return render_template('products/updatebrand.html', title='Update brand Page', updatebrand=updatebrand, form=form)


@products.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)

    if request.method == 'POST':
        db.session.remove(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('main.admin'))
    flash(f'The brand {brand.name} cant be deleted', 'warning')
    return redirect(url_for('main.admin'))


@products.route('/addcat', methods=['GET', 'POST'])
def addcat():
    form = AddCatForm()

    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        getcat = form.name.data
        cat = Category(name=getcat)

        db.session.add(cat)
        flash(f'The Category {getcat} was added to your databse', 'success')
        db.session.commit()
        return redirect(url_for('products.addcat'))

    return render_template('products/addbrand.html', form=form)


@products.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):

    if 'username' not in session:
        flash('Please login first', 'danger')

    form = AddBrandForm()
    updatecat = Category.query.get_or_404(id)
    brand = request.form.get('category')

    if request.method == 'POST':
        updatecat.name = brand
        flash('Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('admin.category'))

    return render_template('products/updatebrand.html', title='Update Category Page', updatecat=updatecat, form=form)


@products.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'The brand {category.name} was deleted from your database', 'success')
        return redirect(url_for('main.admin'))
    flash(f'The brand {category.name} cant be deleted', 'warning')
    return redirect(url_for('main.admin'))


@products.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin.login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProduct()

    if request.method == "POST":
        # Add product into database
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, brand_id=brand,
                            category_id=category, desc=desc, image_1=image_1,
                            image_2=image_2, image_3=image_3)

        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('main.admin'))

    return render_template('products/addproduct.html', title='Add Products Page', form=form, brands=brands,
                           categories=categories)

@products.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddProduct()

    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash('Your product has been updated', 'success')
        return redirect(url_for('main.admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors

    return render_template('products/updateproduct.html', form=form, brands=brands,
                           categories=categories, product=product)


@products.route('/tshirt', methods=['GET', 'POST'])
def tshirt():
    form = OrderForm()
    products = Addproduct.query.all()

    if request.method == 'POST ' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        order = Order(name=name, mobile_num=mobile, order_place=order_place, quantity=quantity, ddate=now_time)
        db.session.add(order)
        db.session.commit()
        flash(f'Order successful', 'success')
        return render_template('products/tshirts.html', tshirt=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        tshirt = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/view_product.html', tshirts=tshirt)
    elif 'order' in request.args:
        product_id = request.args['order']
        tshirt = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/order_product.html', tshirts=tshirt, form=form)

    return render_template('products/tshirts.html', tshirt=products, form=form)


@products.route('/bands', methods=['GET', 'POST'])
def bands():
    form = OrderForm()
    products = Addproduct.query.all()

    if request.method == 'POST ' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        if 'username' in session:
            username = session['username']
            order = Order(name=name, mobile_num=mobile, order_place=order_place, quantity=quantity, ddate=now_time)
            db.session.add(order)
            flash(f'Thanks for your order', 'success')
            db.session.commit()
            return render_template('products/wallet.html', bands=products, form=form)

    if 'view' in request.args:
        product_id = request.args['view']
        bands = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/view_product.html', tshirts=bands)
    elif 'order' in request.args:
        product_id = request.args['order']
        tshirt = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/order_product.html', tshirts=tshirt, form=form)

    return render_template('products/wallet.html', bands=products, form=form)


@products.route('/sunglasses', methods=['GET', 'POST'])
def sunglasses():
    form = OrderForm()
    products = Addproduct.query.all()

    if request.method == 'POST ' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        if 'username' in session:
            username = session['username']
            order = Order(name=name, mobile_num=mobile, order_place=order_place, quantity=quantity, ddate=now_time)
            db.session.add(order)
            flash(f'Thanks for your order', 'success')
            db.session.commit()
            return render_template('products/sunglasses.html', sunglasses=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        sunglasses = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/view_product.html', tshirts=sunglasses)
    elif 'order' in request.args:
        product_id = request.args['order']
        tshirt = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/order_product.html', tshirts=tshirt, form=form)

    return render_template('products/sunglasses.html', sunglasses=products, form=form)


@products.route('/jewelry', methods=['GET', 'POST'])
def jewelry():
    form = OrderForm()
    products = Addproduct.query.all()

    if request.method == 'POST ' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        if 'username' in session:
            username = session['username']
            order = Order(name=name, mobile_num=mobile, order_place=order_place, quantity=quantity, ddate=now_time)
            db.session.add(order)
            flash(f'Thanks for your order', 'success')
            db.session.commit()
            return render_template('products/jewelry.html', jewelry=products, form=form)

    if 'view' in request.args:
        product_id = request.args['view']
        jewelry = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/view_product.html', tshirts=jewelry)
    elif 'order' in request.args:
        product_id = request.args['order']
        tshirt = Addproduct.query.filter_by(id=product_id).all()

        return render_template('products/order_product.html', tshirts=tshirt, form=form)

    return render_template('products/jewelry.html', jewelry=products, form=form)

