import csv
import re
import bcrypt
from tabulate import tabulate
accounts = []

def main():
    show_account()
    print(accounts)
    # email = reg_email()
    # password = reg_password()
    # save_account(email, password)

def reg_email():
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    while True:
        email = input("Write your email: ").strip()
        if bool(re.match(pattern, email)):
            return email
        else:
            print("E-mail must be in right format (example@foo.com)")



def reg_password():

    pattern = r'^(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'

    while True:
        password = input("Write your password: ").strip()
        rewrite_password = input("Rewrite your password: ").strip()
        if bool(re.match(pattern, password)) and password == rewrite_password:
            return password
        elif bool(re.match(pattern, password)) and password != rewrite_password:
            print("Passwords must match")
        else:
            print("Invalid Format\nPassword must contain at least 8 characters 1 number and 1 special character")


def save_account(email, password):
    with open("accounts.csv", "a", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=["Id","E-mail", "Password"])
        account = {}
        account["Id"] = str(len(accounts))
        account["E-mail"] = email
        account["Password"] = password
        writer.writerow(account)
        

def show_account():
    with open("accounts.csv", "r") as file:
        reader = csv.DictReader(file)
        for account in reader:
            accounts.append(account)
    print(tabulate(accounts, headers="keys", tablefmt="grid"))
    

if __name__ == "__main__":
    main()