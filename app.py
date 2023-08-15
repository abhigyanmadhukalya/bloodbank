import mysql.connector
from bloodback_functions import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
    create_tables,
    create_database,
)
from rich.traceback import install
import inquirer

# Better traceback and error logging
install(show_locals=True)


def main():
    create_database()
    create_tables()

    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, name=DB_NAME
    )
    cursor = conn.cursor()

    try:
        questions = [
            inquirer.List(
                "options",
                message="What would you like to do?",
                choices=["Donate Blood", "View blood donors", "Admin Access", "Exit"],
            )
        ]

        answers = inquirer.prompt(questions)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        conn.close()
        cursor.close()
