import inquirer
import mysql.connector
from rich.traceback import install

from bloodbank_functions import perform_action
from models import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
    create_database,
    create_tables,
)

# Better traceback and error logging
install(show_locals=True)


def main():
    while True:
        create_database()
        create_tables()

        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor = conn.cursor()

        try:
            questions = [
                inquirer.List(
                    "options",
                    message="What would you like to do?",
                    choices=[
                        "Donate blood",
                        "View blood donors",
                        "Administrator",
                        "Exit",
                    ],
                )
            ]

            answers = inquirer.prompt(questions)
            perform_action(answers)
        except mysql.connector.Error as e:
            print(f"Something went wrong: {str(e)}")
        finally:
            conn.commit()
            conn.close()
            cursor.close()


if __name__ == "__main__":
    main()
