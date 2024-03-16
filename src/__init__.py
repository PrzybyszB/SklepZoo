from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from views.user_blueprint import user_blueprint
from views.product_blueprint import product_blueprint
from views.cart_blueprint import cart_blueprint
from views.payment_blueprint import payment_blueprint
from views.views_blueprint import views_blueprint
from db_models import init_db, Users, Products, Category, Orders, Orders_detail, Customer

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Ładowanie konfiguracji z pliku config.py
app.config.from_pyfile('config.py')

# Inicjalizacja bazy danych
init_db(app)

# Inicjalizacja Login Managera
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_blueprint.login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Rejestracja blueprintów
app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(cart_blueprint)
app.register_blueprint(payment_blueprint)
app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
