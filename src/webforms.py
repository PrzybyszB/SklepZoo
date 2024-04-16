from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Email, Length
from src.db_models import Category





class LoginForm(FlaskForm):
    email = StringField("Email", validators =[DataRequired()])
    password = PasswordField("Password", validators =[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name =  StringField("Imię", validators=[DataRequired(), Length(max=200)])
    username = StringField("Username", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[DataRequired(), Email(message="Niepoprawny email"), Length(max=120)])
    last_name = StringField("Nazwisko", validators=[DataRequired(), Length(max=200)])
    address = StringField("Adres", validators=[DataRequired(), Length(max=120)])
    password_hash = PasswordField("Hasło", validators=[DataRequired(), EqualTo('password_hash2', message='Hasła nie są takie same!')])
    password_hash2 = PasswordField("Potwierdź hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired()])
    password_hash =  PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ProductForm(FlaskForm):
    product_name = StringField("Nazwa Produktu", validators=[DataRequired(), Length(max=200)])
    cost = IntegerField("Koszt", validators=[DataRequired()])
    producer = StringField("Producent", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Dodaj Produkt")
    
    # Define category choices as loop choices=('category_id', 'category_name'), with current_app.app_context() to work in apllication context
    def get_category_choices():
        with current_app.app_context():
            categories = Category.query.all()
            return [(str(category.category_id), category.category_name) for category in categories]

    
    category_id = SelectField(u'Kategoria', choices=get_category_choices)


class CategoryForm(FlaskForm):
    category_name = StringField("Nazwa Kategorii", validators=[DataRequired(), Length(max=50)])
    category_slug = StringField("Slug Kategorii", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Dodaj Kategorie")


class Order_detailForm(FlaskForm):
    quantity_of_product = IntegerField('Ilość', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Dodaj do koszyka")


class CustomerForm(FlaskForm):
    email =  StringField("Email", validators=[DataRequired(), Email(message="Niepoprawny email"), Length(max=120)]) 
    name = StringField("Imię", validators=[DataRequired(), Length(max=120)]) 
    last_name =StringField("Nazwisko", validators=[DataRequired(), Length(max=120)]) 
    address = StringField("Adres", validators=[DataRequired(), Length(max=120)]) 
    submit = SubmitField("Dalej")


class SearchForm(FlaskForm):
    searched = StringField("Nazwa produktu", validators=[DataRequired()])
    submit = SubmitField("Wyszukaj")