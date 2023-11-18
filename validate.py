import re
import inquirer.errors


def validate_name(_, value):
    if not re.match(r"^[A-Za-z\s]+$", value):
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid name format. Name should only contain letters and spaces.",
        )
    return value


def validate_contact_number(_, value):
    if not re.match(r"^\d{10}$", value):
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid contact number format. Contact number should be 10 digits.",
        )
    return value


def validate_blood_type(value):
    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if value.upper() not in valid_blood_types:
        return "Invalid blood type. Please enter a valid blood type."
    return True

def validate_admin(username):
    try:
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=3306,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your database credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        else:
            print(f"Error connecting to MySQL: {err}")
        return False

    cur = conn.cursor()

    # Check if the provided username exists in the admin table
    cur.execute("SELECT COUNT(*) FROM admins WHERE username = %s", (username,))
    count = cur.fetchone()[0]

    # Close the database connection
    conn.close()

    return count > 0
