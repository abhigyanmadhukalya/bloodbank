import inquirer
import mysql.connector
from random import randint
from rich.console import Console
from rich.table import Table
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from validate import (
    validate_blood_type,
    validate_contact_number,
    validate_name,
)
from admin import admin_action
from sys import exit


def perform_action(answers):
    if answers["options"] == "Donate blood":
        donate_blood()
    elif answers["options"] == "Exit":
        exit()
    elif answers["options"] == "Administrator":
        admin_action()
    elif answers["options"] == "View blood donors":
        questions = [
            inquirer.List(
                "category",
                message="How would you like to view them? ",
                choices=["Entire list", "By name", "By blood type"],
            )
        ]
        answers = inquirer.prompt(questions)
        if answers["category"] == "Entire list":
            view_entire_list()
        elif answers["category"] == "By name":
            view_by_name()
        elif answers["category"] == "By blood type":
            view_by_blood_type()


def donate_blood():
    name = str(
        inquirer.text(
            message="Enter your name",
            validate=validate_name,
        )
    )
    contact_number = str(
        inquirer.text(
            message="Enter your contact number",
            validate=validate_contact_number,
        )
    )
    blood_type = str(
        inquirer.text(message="Enter your blood type", validate=validate_blood_type)
    )
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()

    try:
        while True:
            donor_id = randint(100000, 999999)
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
        values = (name, contact_number, blood_type, donor_id)
        cursor.execute(query, values)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def view_entire_list():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, donor_id, name, blood_type, contact_number FROM donors"
        )
        data = cursor.fetchall()

        console = Console()

        table = Table(title="Entire list of donors")
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
    name = str(
        inquirer.text(
            message="Enter your name",
            validate=validate_name,
        )
    )
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        query = "SELECT id, donor_id, name, blood_type, contact_number from donors WHERE name = %s"
        cursor.execute(query, (name,))
        data = cursor.fetchall()

        console = Console()

        table = Table(title=f"List of people with name: {name}")

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
    blood_type = str(
        inquirer.text(message="Enter your blood type", validate=validate_blood_type)
    )
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        query = "SELECT id, donor_id, name, blood_type, contact_number from donors WHERE blood_type = %s"
        cursor.execute(query, (blood_type,))
        data = cursor.fetchall()

        console = Console()

        table = Table(title=f"List of people with blood type: {blood_type}")

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
