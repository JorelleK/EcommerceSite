from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, TextAreaField, validators, SelectField, StringField, PasswordField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


class AddBrandForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])

    submit = SubmitField('Add Brand')


# Add category
class AddCatForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])

    submit = SubmitField('Add Category')


class AddProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png', 'gif', 'jpeg']), 'images only please'])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'images only please'])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg']), 'images only please'])

    submit = SubmitField('Add Product')


class OrderForm(FlaskForm):  # Create Order Form
    name = StringField('', validators=[DataRequired(), Length(min=2, max=30)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('', validators=[DataRequired(), Length(min=2, max=30)],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('', validators=[DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('',  validators=[DataRequired(), Length(min=2, max=30)],
                              render_kw={'placeholder': 'Order Place'})