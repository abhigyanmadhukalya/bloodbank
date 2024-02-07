import mysql.connector
from models import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def admin_register(username: str, password: str) -> None:
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*) FROM admins WHERE username = %s;
            """,
            (username,),
        )
        if cursor.fetchone()[0] != 0:
            print(f"Username {username} already exists.")
        else:
            query = """
                INSERT INTO admins (username, password) VALUES (%s, %s);
            """
            values = (username, password)
            cursor.execute(query, values)
            print("Registration successful")
    except mysql.connector.Error as e:
        print(f"Something went wrong: {str(e)}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def admin_sign_in(username: str, password: str):
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM admins WHERE username = %s;
            """,
            (username,),
        )
        admin = cursor.fetchone()
        if admin is None:
            print(f"Username {username} does not exist.")
        else:
            if password == admin[2]:
                print("Success")
            else:
                print("Incorrect password")
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def delete_donor_table():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
    drop table donors;
    """
        )
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def modify_donor_table():
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    try:
        pass
    except mysql.connector.Error as e:
        print(f"Something went wrong: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
