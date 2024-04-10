from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Email
from src.db_models import Category





class LoginForm(FlaskForm):
    email = StringField("Email", validators =[DataRequired()])
    password = PasswordField("Password", validators =[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name =  StringField("Imię", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Niepoprawny email")])
    last_name = StringField("Nazwisko", validators=[DataRequired()])
    address = StringField("Adres", validators=[DataRequired()])
    password_hash = PasswordField("Hasło", validators=[DataRequired(), EqualTo('password_hash2', message='Hasła nie są takie same!')])
    password_hash2 = PasswordField("Potwierdź hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password_hash =  PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ProductForm(FlaskForm):
    product_name = StringField("Nazwa Produktu", validators=[DataRequired()])
    cost = IntegerField("Koszt", validators=[DataRequired()])
    producer = StringField("Producent", validators=[DataRequired()])
    submit = SubmitField("Dodaj Produkt")
    
    # Define category choices as loop choices=('category_id', 'category_name'), with current_app.app_context() to work in apllication context
    def get_category_choices():
        with current_app.app_context():
            categories = Category.query.all()
            return [(str(category.category_id), category.category_name) for category in categories]

    
    category_id = SelectField(u'Kategoria', choices=get_category_choices)


class CategoryForm(FlaskForm):
    category_name = StringField("Nazwa Kategorii", validators=[DataRequired()])
    category_slug = StringField("Slug Kategorii", validators=[DataRequired()])
    submit = SubmitField("Dodaj Kategorie")


class Order_detailForm(FlaskForm):
    quantity_of_product = IntegerField('Ilość', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Dodaj do koszyka")


class CustomerForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired(), Email(message="Niepoprawny email")]) 
    name = StringField("Imię", validators=[DataRequired()]) 
    last_name =StringField("Nazwisko", validators=[DataRequired()]) 
    address = StringField("Adres", validators=[DataRequired()]) 
    submit = SubmitField("Dalej")


class SearchForm(FlaskForm):
    searched = StringField("Nazwa produktu", validators=[DataRequired()])
    submit = SubmitField("Wyszukaj")