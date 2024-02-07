import mysql.connector
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def admin_register(username: str, password: str) -> None:
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
        select count(*) from admins where username = {username};
        """
        )
        if cursor.fetchone()[0] == 0:
            print(f"Username {username} does not exist.")
        else:
            query = """
                insert into admins (username, password) values (%s, %s)
            """
            values = (username, password)
            cursor.execute(query, values)
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def admin_sign_in(username: str, password: str):
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""
            select count(*) from admins where username = {username};
            """
        )
        if cursor.fetchone()[0] == 0:
            print(f"Username {username} does not exist.")
        users = cursor.fetchall()
        if username == users[0][1]:
            if password == users[0][2]:
                print("success")
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
