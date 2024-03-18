#Hard programming your stuff

class Config:
    SECRET_KEY = "test haslo"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/SklepZooDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'development'
    FLASK_APP= 'src'
    FLASK_DEBUG=1
    SWAGGER = {
        "title": "SklepZooApi",
        "uiversion": 3
    }
# import os

# This is when this repo goin into net, and u dont want reveal SECRET_KEY or other stuff which are into your runtime environment.

# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
#         or 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/FirstDataBase'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
