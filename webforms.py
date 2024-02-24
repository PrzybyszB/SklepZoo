from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Optional




#Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators =[DataRequired()])
    password = PasswordField("Password", validators =[DataRequired()])
    submit = SubmitField("Submit")



#Create a User Form Class
class UserForm(FlaskForm):
    name =  StringField("Imię", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email =  StringField("Email", validators=[DataRequired()])
    last_name = StringField("Nazwisko", validators=[Optional()])
    adress = StringField("Adres", validators=[Optional()])
    password_hash = PasswordField("Hasło", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Potwierdź hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Password Form Class
class PasswordForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password_hash =  PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Product Form Class
class ProductForm(FlaskForm):
    product_name = StringField("Nazwa Produktu", validators=[DataRequired()])
    cost = IntegerField("Koszt", validators=[DataRequired()])
    producent = StringField("Producent", validators=[DataRequired()])
    submit = SubmitField("Dodaj Produkt")
    category_id = SelectField(u'Kategoria', choices=[('1', 'Sucha Karma'), 
                                                       ('2', 'Mokra Karma'),
                                                        ('3', 'Zabawki')])

class CategoryForm(FlaskForm):
    category_name = StringField("Nazwa Kategorii", validators=[DataRequired()])
    submit = SubmitField("Dodaj Kategorie")

class Order_detailForm(FlaskForm):
    quantity_of_product = IntegerField('Ilość', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Dodaj do koszyka")


class CustomerForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()]) 
    name = StringField("Imię", validators=[DataRequired()]) 
    last_name =StringField("Nazwisko", validators=[DataRequired()]) 
    adress = StringField("Adres", validators=[DataRequired()]) 
    submit = SubmitField("Dalej")