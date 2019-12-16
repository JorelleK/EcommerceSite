from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from shop.customers.models import Customer


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_user(self, username):
        customer = Customer.query.filter_by(username=username.data).first()
        if customer is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer is not None:
            raise ValidationError('Email is taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        customer = Customer.query.filter_by(username=username.data).first()
        if customer is None:
            raise ValidationError('That username does not exist in our database.')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            customer = Customer.query.filter_by(username=username.data).first()
            if customer is not None:
                raise ValidationError('That username is already taken')


