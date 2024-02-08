from os import environ
from typing import Any

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection

# Remember to add these to your environmental variables
DB_HOST = "localhost"
DB_USER = environ["mysql_username"]
DB_PASSWORD = environ["mysql_password"]
DB_NAME = "bloodbank"


def create_database() -> None:
    try:
        conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD
        )
        cursor: MySQLCursorAbstract | Any = conn.cursor()

        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

        conn.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection

    except mysql.connector.Error as e:
        print(f"Something went wrong during database creation: {str(e)}")


def create_tables() -> None:
    try:
        conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor: MySQLCursorAbstract | Any = conn.cursor()

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

        # Create admins table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
            """
        )

        conn.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection

    except mysql.connector.Error as e:
        print(f"Something went wrong during DB initialization: {str(e)}")
