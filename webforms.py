from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length



#Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators =[DataRequired()])
    password = PasswordField("Password", validators =[DataRequired()])
    submit = SubmitField("Submit")



#Create a User Form Class
class UserForm(FlaskForm):
    name =  StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email =  StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Password Form Class
class PasswordForm(FlaskForm):
    email =  StringField("What's Your Email", validators=[DataRequired()])
    password_hash =  PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Product Form Class
class ProductForm(FlaskForm):
    product_name = StringField("Nazwa Produktu", validators=[DataRequired()])
    cost = IntegerField("Koszt", validators=[DataRequired()])
    producent = StringField("Producent", validators=[DataRequired()])
    data_added = StringField("Data dodania", validators=[DataRequired()])
    submit = SubmitField("Dodaj Produkt")
