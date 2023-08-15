import mysql.connector

def perform_action(answers: str):
    if answers == "Donate blood":
        name = str(input("Enter your name: "))
        contact_number = str(input("Enter your contact number: "))
        blood_type = str(input("Enter your blood type: "))
        donate_blood(name, contact_number, blood_type)


def donate_blood(name: str, contact_number: str, blood_type: str):
    pass
