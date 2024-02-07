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


def validate_blood_type(_, value):
    valid_blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if value.upper() not in valid_blood_types:
        return "Invalid blood type. Please enter a valid blood type."
    return True


def validate_username(_, value):
    if not re.match(r"^[a-zA-Z0-9_]{3,16}$", value):
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid username format.",
        )
    return value


def validate_password(_, value):
    if not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value
    ):
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid password format.",
        )
    return value

