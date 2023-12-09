import mysql.connector
from os import environ
from dotenv import load_dotenv

load_dotenv()

# Remember to add these to your environmental variables
DB_HOST = "localhost"
DB_USER = environ["mariadb_username"]
DB_PASSWORD = environ["mariadb_password"]
DB_NAME = "bloodbank"


def create_database():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

        conn.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection

    except mysql.connector.Error as e:
        print(f"Something went wrong during database creation: {str(e)}")


def create_tables():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor = conn.cursor()

        # Create donors table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS donors (
        id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                blood_type VARCHAR(3) NOT NULL,
                contact_number VARCHAR(15),
                donor_id INT UNIQUE
            )
            """
        )

        conn.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection

    except mysql.connector.Error as e:
        print(f"Something went wrong during DB initialization: {str(e)}")
