import csv
import re
import bcrypt
from tabulate import tabulate


accounts = []

def main():
    login_or_register()

def register_email():
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        try:
            email = input("Write your email: ").strip().lower()
            if check_email(email) and bool(re.match(pattern, email)):
                return email
            else:
                print("E-mail must be in right format (example@foo.com)")

            with open("accounts.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in list(reader):
                    if row["E-mail"] == email:
                        print("This email already exists,\ntry something else")
                        
        except EOFError:
            print("Invalid input")
            continue

def register_password():
    pattern = r'^(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'
    while True:
        password = input("Write your password: ").strip()
        rewrite_password = input("Rewrite your password: ").strip()
        if bool(re.match(pattern, password)) and password == rewrite_password:
            return hash_password(password)
        elif bool(re.match(pattern, password)) and password != rewrite_password:
            print("Passwords must match")
        else:
            print("Invalid Format\nPassword must contain at least 8 characters 1 number and 1 special character")

def register_account():
    with open("accounts.csv", "a+", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=["E-mail","Password", "Id"])
        account = {}
        if file.tell() == 0:
            writer.writeheader()
        account["E-mail"] = register_email()
        account["Password"] = register_password() 
        accounts.append(account)
        account["Id"] = len(show_accounts())
        writer.writerows(accounts)

def show_accounts():
    with open("accounts.csv", "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def login_account(logged = False):
    while True:
        email = input("Write your email: ")
        password = input("Write your password: ")
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            for account in list(reader):
                if account["E-mail"] == email and account["Password"] == password:
                    print(f"Logged in succsessfully as {email}")
                    logged = True
                    return logged
                else:
                    print("Wrong password or email")

def check_email(email):
    with open("accounts.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in list(reader):
            if row["E-mail"] == email:
                print("This email already exists,\ntry something else")
                return False
            else:
                return True

def login_or_register():
    text = input("Type what to do (Login or Register): ")
    if text == "login":
        login_account()
    elif text == "register":
        register_account()
    else:
        print("Invalid input")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    main()