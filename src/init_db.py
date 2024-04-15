#Creating DB MySQL
import mysql.connector


#MySQL Docker 
mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    passwd="123A."
)


my_cursor = mydb.cursor()


my_cursor.execute("CREATE DATABASE IF NOT EXISTS SklepZooDB")   # Uncomment this before create db

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)