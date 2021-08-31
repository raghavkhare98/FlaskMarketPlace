from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email_address(selfs, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email is already registered! Please try a different email address.')
    """
    in the above line we made a function which will run a query on the User database to return any matches that are present in the database
    which matches with a new user being created. We write first because the user variable will return an object so to display the username
    we use first(). The FlaskForm class will chec the function name and will try to find any fields that contain the same name as the function
    or a part of the function, here username, matches with the username field and hence FlaskForm will a query against username
    """
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()]) #here validators are in a list because
    #validators takes only 1 argumen and to pass 2 arguments, we added them in a list.
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Enter your username:', validators=[DataRequired()])
    password = PasswordField(label='Enter your password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')