from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)


#Create Model
class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String(120), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    orders_relationship = db.relationship('Orders', backref='users', lazy=True)


    # 
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    

    @property
    def is_anonymous(self):
        return False
    
    # Doing changes about user_id define, default is define as id in login stuff
    def get_id(self):
        return (self.user_id)
    
    @property
    def is_anonymous(self):
        return False


    # Resolve : sqlalchemy.exc.InvalidRequestError: Entity namespace for "users" has no property "id"
    @property
    def id(self):
        return self.user_id
    
    # Doing password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError ('password is not readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, "pbkdf2:sha256")
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, index=True)
    category_name =db.Column(db.String(50), unique=True, nullable=False)
    category_slug =db.Column(db.String(50), unique=True, nullable=False)
    products_relationship = db.relationship('Products', backref='category', lazy=True)

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False, unique=True)
    cost = db.Column(db.Integer, nullable=False)
    producer = db.Column(db.String(200), nullable=False)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    # TODO category_name = db.Column(db.Integer, db.ForeignKey('category.category_name'), nullable=False,)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False,)
    order_detail_relationship = db.relationship('Orders_detail', backref='products', lazy=True)
    
class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True,)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=True,)
    order_data = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Integer, nullable=False)
    order_detail_relationship = db.relationship('Orders_detail', backref='orders', lazy=True)

class Orders_detail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=True,)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    quantity_of_product = db.Column(db.Integer, nullable=False)
    
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    deleted_at = db.Column(db.DateTime)
    order_detail_relationship = db.relationship('Orders', backref='customer', lazy=True)
