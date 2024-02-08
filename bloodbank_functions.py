from random import randint
from sys import exit
from typing import Any, Dict, List

import inquirer
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.types import RowItemType, RowType
from rich.console import Console
from rich.table import Table

from admin import admin_action
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from validate import (
    validate_blood_type,
    validate_contact_number,
    validate_name,
)


def perform_action(answers):
    if answers["options"] == "Donate blood":
        donate_blood()
    elif answers["options"] == "Exit":
        exit()
    elif answers["options"] == "Administrator":
        admin_action()
    elif answers["options"] == "View blood donors":
        questions: list = [
            inquirer.List(
                "category",
                message="How would you like to view them? ",
                choices=["Entire list", "By name", "By blood type"],
            )
        ]
        answers: dict[Any, Any] | None = inquirer.prompt(questions)
        if answers["category"] == "Entire list":
            view_entire_list()
        elif answers["category"] == "By name":
            view_by_name()
        elif answers["category"] == "By blood type":
            view_by_blood_type()


def donate_blood():
    name: str = str(
        inquirer.text(
            message="Enter your name",
            validate=validate_name,
        )
    )
    contact_number: str = str(
        inquirer.text(
            message="Enter your contact number",
            validate=validate_contact_number,
        )
    )
    blood_type: str = str(
        inquirer.text(message="Enter your blood type", validate=validate_blood_type)
    )
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()

    try:
        while True:
            donor_id: int = randint(100000, 999999)
            # Check if the generated donor ID already exists
            cursor.execute(
                "SELECT COUNT(*) FROM donors WHERE donor_id = %s", (donor_id,)
            )
            if cursor.fetchone()[0] == 0:
                break  # Unique donor ID found, exit the loop
        query = """
        INSERT INTO donors (name, contact_number, blood_type, donor_id)
        VALUES (%s, %s, %s, %s);
        """
        values: tuple[str, str, str, int] = (name, contact_number, blood_type, donor_id)
        cursor.execute(query, values)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def view_entire_list():
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, donor_id, name, blood_type, contact_number FROM donors"
        )
        data: List[RowType | Dict[str, RowItemType]] | Any = cursor.fetchall()

        console: Console = Console()

        table: Table = Table(title="Entire list of donors")

        table.add_column("ID")
        table.add_column("Donor ID")
        table.add_column("Name")
        table.add_column("Blood Type")
        table.add_column("Contact Number")

        for id, donor_id, name, blood_type, contact_number in data:
            table.add_row(
                str(id), str(donor_id), str(name), str(blood_type), str(contact_number)
            )

        console.print(table)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def view_by_name():
    name: str = str(
        inquirer.text(
            message="Enter your name",
            validate=validate_name,
        )
    )
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        query = "SELECT id, donor_id, name, blood_type, contact_number from donors WHERE name = %s"
        cursor.execute(query, (name,))
        data: List[RowType | Dict[str, RowItemType]] | Any = cursor.fetchall()

        console: Console = Console()

        table: Table = Table(title=f"List of people with name: {name}")

        table.add_column("ID")
        table.add_column("Donor ID")
        table.add_column("Name")
        table.add_column("Blood Type")
        table.add_column("Contact Number")

        for id, donor_id, name, blood_type, contact_number in data:
            table.add_row(
                str(id), str(donor_id), str(name), str(blood_type), str(contact_number)
            )

        console.print(table)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def view_by_blood_type():
    blood_type: str = str(
        inquirer.text(message="Enter your blood type", validate=validate_blood_type)
    )
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        query = "SELECT id, donor_id, name, blood_type, contact_number from donors WHERE blood_type = %s"
        cursor.execute(query, (blood_type,))
        data: List[RowType | Dict[str, RowItemType]] | Any = cursor.fetchall()

        console: Console = Console()

        table: Table = Table(title=f"List of people with blood type: {blood_type}")

        table.add_column("ID")
        table.add_column("Donor ID")
        table.add_column("Name")
        table.add_column("Blood Type")
        table.add_column("Contact Number")

        for id, donor_id, name, blood_type, contact_number in data:
            table.add_row(
                str(id), str(donor_id), str(name), str(blood_type), str(contact_number)
            )

        console.print(table)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def modify_entry_to_donor_table(
    name: str, contact_number: str, blood_type: str, old_name: str
):
    conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor: MySQLCursorAbstract | Any = conn.cursor()
    try:
        cursor.execute(
            """
            update donors set name = %s, contact_number = %s, blood_type = %s where name = %s;
            """,
            (name, contact_number, blood_type, old_name),
        )
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
