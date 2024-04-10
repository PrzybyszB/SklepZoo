#Creating DB MySQL
import mysql.connector

#SELF
# mydb = mysql.connector.connect(
#     host="mysq",
#     user="pbartosz",
#     passwd="1q2w3e4r5t6Y."
# )

#MySQL Docker 
mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    passwd="123A."
)


my_cursor = mydb.cursor()

# flask db init

# flask db migrate -m "Initial migration."

# flask db upgrade

my_cursor.execute("CREATE DATABASE IF NOT EXISTS SklepZooDB")   # Uncomment this before create db

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)