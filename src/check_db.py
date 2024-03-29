import mysql.connector

def check_db(host, user, password, database):
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        conn.close()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1049:  # 1049 = Database doesn't exist
            return False
        else:
            raise

# Connection with db
host = 'mysql'
user = 'root'
password = '123A.'
database = 'SklepZooDB'

if check_db(host, user, password, database):
    print("Database exist")
else:
    print("Database doesn't exist")