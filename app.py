from typing import Any, NoReturn

import inquirer
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection
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


def main() -> NoReturn:
    while True:
        create_database()
        create_tables()

        conn: PooledMySQLConnection | MySQLConnectionAbstract = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor: MySQLCursorAbstract | Any = conn.cursor()

        try:
            questions: list = [
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

            answers: dict[Any, Any] | None = inquirer.prompt(questions)
            perform_action(answers)
        except mysql.connector.Error as e:
            print(f"Something went wrong: {str(e)}")
        finally:
            conn.commit()
            conn.close()
            cursor.close()


if __name__ == "__main__":
    main()
