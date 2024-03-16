import os


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pbartosz:1q2w3e4r5t6Y.@localhost/FirstDataBase'

SECRET_KEY = "test haslo"

SQLALCHEMY_MIGRATE_REPO = os.path.join("/home/pbartosz/Programowanie/Projekty/Sklep_zoo", 'migrations')