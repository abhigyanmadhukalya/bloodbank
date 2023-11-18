import bcrypt
import mysql.connector
from mysql.connector import errorcode
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

def admin_login(username, password):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            user="DB_USER",
            password="DB_PASSWORD",
            host="DB_HOST",
            port=3306,
            database="DB_NAME"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your database credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        else:
            print(f"Error connecting to MySQL: {err}")
        return

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Retrieve hashed password from the database for the given username
    cur.execute("SELECT password FROM admin WHERE username = %s", (username,))
    row = cur.fetchone()

    if row:
        hashed_password = row[0].encode('utf-8')

        # Check if the provided password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Login successful. Welcome, Admin!")
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Admin account not found.")

    # Close the database connection
    conn.close()
