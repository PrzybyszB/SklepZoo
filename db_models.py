# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from app import app
# from datetime import datetime

# db = SQLAlchemy(app)


# class Users(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     data_added = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Doing password stuff
#     password_hash = db.Column(db.String(128))
#     password_hash - db.Column(db.String(128))

#     @property
#     def password(self):
#         raise AttributeError ('password is not readable attribute')
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
#     def verify_password(self,password):
#         return check_password_hash(self.password_hash, password)
#     # Create A String
#     def __repr__(self):
#         return '<Name %r>' % self.name

# class Products(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String(200), nullable=False)
#     cost = db.Column(db.Integer, nullable=False)
#     producent = db.Column(db.String(200), nullable=False)
#     data_added = db.Column(db.DateTime, default=datetime.utcnow)

#     # Create A String
#     def __repr__(self):
#         return '<Name %r>' % self.name