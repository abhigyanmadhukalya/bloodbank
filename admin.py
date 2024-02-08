from getpass import getpass
from typing import Any, Dict

import inquirer
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.types import RowItemType, RowType
import bloodbank_functions
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from validate import (
    validate_blood_type,
    validate_contact_number,
    validate_name,
    validate_password,
    validate_username,
)


def admin_action():
    questions: list = [
        inquirer.List(
            "category",
            message="What would you like to do?",
            choices=["Admin Sign in", "Admin Register"],
        )
    ]
    answers: dict[Any, Any] | None = inquirer.prompt(questions)
    if answers["category"] == "Admin Sign in":
        admin_sign_in()
        admin_tasks()

    if answers["category"] == "Admin Register":
        admin_register()


def admin_tasks():
    questions: list = [
        inquirer.List(
            "job",
            message="What would you like to do?",
            choices=["Delete donor data", "Modify donor data"],
        )
    ]
    answers: dict[Any, Any] | None = inquirer.prompt(questions)
    if answers["job"] == "Delete donor data":
        delete_donor_table()
    elif answers["job"] == "Modify donor data":
        modify_donor_table()


def admin_register() -> None:
    username: str = str(
        inquirer.text(
            message="Enter username",
            validate=validate_username,
        )
    )
    password: str = str(
        inquirer.text(message="Enter password", validate=validate_password)
    )

    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*) FROM admins WHERE username = %s;
            """,
            (username,),
        )
        if cursor.fetchone()[0] != 0:
            print(f"Username '{username}' already exists.")
        else:
            query = """
                INSERT INTO admins (username, password) VALUES (%s, %s);
            """
            values: tuple[str, str] = (username, password)
            cursor.execute(query, values)
            print("Registration successful")
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def admin_sign_in():
    username = str(
        inquirer.text(
            message="Enter username",
            validate=validate_username,
        )
    )
    password: str = getpass(prompt="Enter password: ")
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM admins WHERE username = %s;
            """,
            (username,),
        )
        admin: RowType | Dict[str, RowItemType] | Any | None = cursor.fetchone()
        if admin is None:
            print(f"Username '{username}' does not exist.")
        else:
            if password == admin[2]:
                print("Success")
            else:
                print("Incorrect password")
                exit()
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def delete_donor_table():
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        yes_or_no: str = str(input("Are you sure? Y/N"))
        if yes_or_no in "Yy":
            cursor.execute(
                """
        drop table donors;
        """
            )
            print("Donor data deleted successfully.")
        elif yes_or_no in "Nn":
            print("Deletion cancelled.")
        else:
            print("Incorrect answer to question. Answer with Yes(Y) or No(N)")
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def modify_donor_table():
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        name: str = str(
            inquirer.text(message="Enter name to modify entry", validate=validate_name)
        )
        cursor.execute(
            """
            select count(*) from donors where name = %s
            """,
            (name,),
        )
        donors: RowType | Dict[str, RowItemType] | Any | None = cursor.fetchone()
        if donors is None:
            print(f"'{name.capitalize()}' is not a donor")
        new_name: str = str(
            inquirer.text(message="Enter new name for donor: ", validate=validate_name)
        )
        new_contact_number: str = str(
            inquirer.text(
                message="Enter new contact number for donor: ",
                validate=validate_contact_number,
            )
        )
        new_blood_type: str = str(
            inquirer.text(
                message="Enter new blood type for donor: ", validate=validate_blood_type
            )
        )
        bloodbank_functions.modify_entry_to_donor_table(
            new_name, new_contact_number, new_blood_type, name
        )
        print("Successful")

    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
