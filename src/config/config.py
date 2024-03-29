#Hard programming your stuff

# class Config:
#     SECRET_KEY = "test haslo"
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/SklepZooDB'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SWAGGER = {
#         "title": "SklepZooApi",
#         "uiversion": 3
#     }



# This is when this repo goin into net, and u dont want reveal SECRET_KEY or other stuff which are into your runtime environment.

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/SklepZooDB'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "title": "SklepZooApi",
        "uiversion": 3
    }
