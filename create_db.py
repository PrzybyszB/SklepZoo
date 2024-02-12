#Creating FirstDataBase MySQL


import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="pbartosz",
    passwd="1q2w3e4r5t6Y."
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE FirstDataBase")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)