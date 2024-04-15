from datetime import timedelta
from flask import Flask, session
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flasgger import Swagger
from src.myadmin import MyAdminIndexView
from src.views.user_blueprint import user_blueprint
from src.views.product_blueprint import product_blueprint
from src.views.cart_blueprint import cart_blueprint
from src.views.payment_blueprint import payment_blueprint
from src.views.views_blueprint import views_blueprint
from src.api.api_cart_blueprint import api_cart_blueprint
from src.api.api_user_blueprint import api_user_blueprint
from src.api.api_product_blueprint import api_product_blueprint
from src.api.api_payment_blueprint import api_payment_blueprint
from src.api.api_views_blueprint import api_views_blueprint
from src.db_models import db, init_db, Users, Category, Products, Orders, Orders_detail
from src.webforms import SearchForm
from src.config.config import Config
from src.config.swagger import template, swagger_config
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(config_class=Config):
    # Initialize flask app
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # Initialize swagger
    swagger = Swagger(app, template=template, config=swagger_config)

    # Config
    app.config.from_object(config_class)
    
    # Initialize data base
    init_db(app)

    # Initialize Migrate
    migrate = Migrate(app, db)


    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_blueprint.login'
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    
    # Initialize Admin panel
    admin = Admin(app, name='Admin',index_view=MyAdminIndexView(), template_mode='bootstrap3')

    admin.add_view(ModelView(Products, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Orders_detail, db.session))
    admin.add_view(ModelView(Orders, db.session))
        
    # Register Blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(payment_blueprint)
    app.register_blueprint(views_blueprint)

    app.register_blueprint(api_user_blueprint)
    app.register_blueprint(api_product_blueprint)
    app.register_blueprint(api_cart_blueprint)
    app.register_blueprint(api_payment_blueprint)
    app.register_blueprint(api_views_blueprint)
    

    # Flask before request
    @app.context_processor
    def inject_global_variables():
        categories = Category.query.all()
        if categories:
            return {'categories': categories}
        return {'categories': []}
    
    # Search 
    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    # Session time 
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1440)

    return app

