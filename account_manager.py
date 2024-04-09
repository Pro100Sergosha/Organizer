import csv
import os

import re
import bcrypt

from tabulate import tabulate
from colorama import init, Fore, Back, Style

from to_do_app import ToDoApp
from contacts import Contacts
from calculator import Calculator
from weather import WeatherForecast
from rate import Rate
from styles import Styles

# This is a Python program that manages user accounts and provides various functionalitiesю

# The program is structured into several classes:

# 1. AccountManager: Manages user accounts, including registration, login, logout, and account settings.
# 2. ToDoApp: Manages tasks for a logged-in user, including adding, marking as completed, showing, and deleting tasks.
# 3. Contacts: Manages contacts for a logged-in user, including adding, showing, finding, and deleting contacts.
# 4. Calculator: Provides basic calculator functionalities like addition, subtraction, multiplication, division, percentage, square root, and square operations.
# 5. WeatherForecast: Retrieves and displays weather forecast information for a specific city for a specified number of days.
# 6. Rate: Converts currency between Georgian Lari (GEL) and other currencies.

# The main functionality is accessible through a menu-driven interface:

# - Register a new account: Allows users to create a new account with a unique nickname, email, and password.
# - Show the list of accounts: Displays the list of registered accounts with their IDs, nicknames, and emails.
# - Log in: Allows users to log in with their registered email and password.
# - Logout: Logs out the current user.
# - Applications: Provides access to different applications like the to-do list, contacts, calculator, weather forecast, and currency rate converter.
# - Account Settings: Allows logged-in users to change their nickname, password, email, and list format settings.
# - Style Settings: Allows users to customize the font color, font style, and background color for the terminal output.

# Overall, this program serves as a comprehensive tool for managing user accounts and accessing various productivity and utility applications.

class AccountManager:
    def __init__(self, filename="accounts.csv"):
        self.filename = filename
        self.current_id = None
        self.fieldnames = ["ID", "Nickname", "Email", "Password"]
        self.email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.password_regex = r"^(?=.*\d)(?=.*[!@#$%^&*()])(?=.*[a-zA-Z]).{8,}$"
        self.logged_in = False
        self.current_email = None
        self.current_account = None


        self._style_menu = Styles()

    def validate_email(self, email):
        return re.match(self.email_regex, email)


    def validate_password(self, password):
        return re.match(self.password_regex, password)


    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


    def save_account(self, nickname, email, password):
        if not self.validate_email(email):
            print("Invalid Email format.")
            return

        if not self.validate_password(password):
            print("Password must contain at least 8 characters, including one digit and one special character.")
            return
        self.check_file_exists(self.filename, self.fieldnames)

        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Email"] == email:
                    print("An account with this Email already exists.")
                    return

        next_id = 0

        if os.path.exists(self.filename) and os.stat(self.filename).st_size != 0:
            with open(self.filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                ids = [int(row["ID"]) for row in reader]
                next_id = len(ids) + 1

        hashed_password = self.hash_password(password)

        
        with open(self.filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if os.stat(self.filename).st_size == 0:
                writer.writeheader()
            writer.writerow({"ID": next_id, "Nickname": nickname, "Email": email, "Password": hashed_password.decode()})
            print("You've registered!")

 

    def account(self, current_id):
        with open("accounts.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, val in row.items():
                    if val == current_id:
                        return row
            return


    def email_exists(self, email):
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Email"] == email:
                    return True
        return False


    def check_file_exists(self, filename, fieldnames):
        if not os.path.exists(filename):
            with open(filename, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()


    def show_accounts(self):
        self.check_file_exists(self.filename, self.fieldnames)
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            accounts = []
            for row in reader:
                accounts.append([row["ID"], row["Nickname"], row["Email"]])
            return tabulate(accounts, headers=["ID", "Nickname", "Email", "Password"], tablefmt = self._style_menu.list_format())


    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))




    def login(self, email, password):
        self.check_file_exists(self.filename, self.fieldnames)
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in list(reader):
                if row["Email"] == email and self.check_password(password, row["Password"]):
                    self.logged_in = True
                    self.current_email = email
                    self.current_id = row["ID"]
                    self.current_account = row
                    return True
            self._style_menu.new_print("Wrong password or email")

        return False

    def logout(self):
        self.logged_in = False
        self.current_email = None

    

    def change_password(self):
        if not self.logged_in:
            self._style_menu.new_print("You need to log in to change your password.")
            return

        new_password = input("Enter your new password: ")
        if not self.validate_password(new_password):
            self._style_menu.new_print("Password must contain at least 8 characters, including one digit and one special character.")
            return

        hashed_password = self.hash_password(new_password)

        accounts = []
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accounts.append(row)

        updated_accounts = []
        for account in accounts:
            if account["Email"] == self.current_email:
                account["Password"] = hashed_password.decode()
            updated_accounts.append(account)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in updated_accounts:
                writer.writerow(account)
        self._style_menu.new_print("Password successfully updated.")


    def change_email(self):
        if not self.logged_in:
            self._style_menu.new_print("You need to log in to change your email.")
            return

        new_email = input("Enter your new email: ")
        if not self.validate_email(new_email):
            self._style_menu.new_print("Invalid Email format.")
            return

        if self.email_exists(new_email):
            self._style_menu.new_print("User with this Email already exists.")
            return

        accounts = []
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accounts.append(row)

        updated_accounts = []
        for account in accounts:
            if account["Email"] == self.current_email:
                account["Email"] = new_email
            updated_accounts.append(account)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in updated_accounts:
                writer.writerow(account)
        self._style_menu.new_print("Email successfully updated.")


    def change_nickname(self):
        if not self.logged_in:
            self._style_menu.new_print("You need to log in to change your nickname.")
            return
        new_nickname = input("Enter your new nickname: ")
        accounts = []
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accounts.append(row)

        updated_accounts = []
        for account in accounts:
            if account["Email"] == self.current_email:
                account["Nickname"] = new_nickname
            updated_accounts.append(account)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in updated_accounts:
                writer.writerow(account)
        self._style_menu.new_print("Nickname successfully updated.")


    def delete_account(self, email):
        accounts = []
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Email"] != email:
                    accounts.append(row)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in accounts:
                writer.writerow(account)
        self.current_email = None
        self.logged_in = False
        self._style_menu.new_print("Account deleted.")
    

    def account_settings_menu(self):
        if self.logged_in:
            self._style_menu.new_print("\nSettings")
            self._style_menu.new_print("1. Change nickname")
            self._style_menu.new_print("2. Change password")
            self._style_menu.new_print("3. Change email")
            self._style_menu.new_print("4. Delete account")
            self._style_menu.new_print("5. Return to the main menu")
            setting_choice = input("Select an action: ")
            if setting_choice == "1":
                self.change_nickname()
            elif setting_choice == "2":
                self.change_password()
            elif setting_choice == "3":
                self.change_email()
            elif setting_choice == "4":
                password = input("Enter your password: ")
                rewrite_password = input("Rewrite your password: ")
                current_password = self.account(self.current_id)['Password']
                if password == rewrite_password and bcrypt.checkpw(password.encode('utf-8'), current_password.encode('utf-8')):
                    self.delete_account(self.current_email)
                else:
                    self._style_menu.new_print("Email does not exist")
            elif setting_choice == "5":
                self._style_menu.new_print("Returning to the main menu")
            else:
                self._style_menu.new_print("Invalid input. Please select an action again.")
        else:
            self._style_menu.new_print("You need to log in to access settings.")


    def main(self):
        while True:
            if self.current_email == None:
                self._style_menu.new_print("Not logged in")
            else:
                self._style_menu.new_print(f"Logged in as {self.current_email}")
            self._style_menu.new_print("\nMain menu")
            self._style_menu.new_print("1. Register a new account")
            self._style_menu.new_print("2. Show the list of accounts")
            self._style_menu.new_print("3. Log in")
            self._style_menu.new_print("4. Logout")
            self._style_menu.new_print("5. Applications")
            self._style_menu.new_print("6. Account Settings")
            self._style_menu.new_print("7. Style Settings")
            self._style_menu.new_print("8. Exit")   
            choice = input("Enter your choice: ")    
            if choice == "1":
                nickname = input("Enter your Nickname: ")
                if nickname == "":
                    self._style_menu.new_print("Nickname must be filled in.")
                    continue
                elif len(nickname) < 3:
                    self._style_menu.new_print("Nickname length must be more than 3 characters.")
                    continue
                else:
                    email = input("Enter your Email: ").lower()
                    if not self.validate_email(email):
                        self._style_menu.new_print("Invalid Email format.")
                        continue
                    password = input("Enter your password: ")
                    rewrite_password = input("Rewrite your password: ")
                    if not self.validate_password(password):
                        self._style_menu.new_print("Password must contain at least 8 characters, including one digit and one special character.")
                        continue
                    elif password != rewrite_password:
                        self._style_menu.new_print("Passwords must match")
                        continue
                    self.save_account(nickname, email, password)
            elif choice == "2":
                self._style_menu.new_print(self.show_accounts())
            elif choice == "3":
                email = input("Enter your Email: ")
                password = input("Enter your password: ")
                self.login(email, password)
            elif choice == "4":
                self.logout()
            elif choice == "5":
                if self.current_email == None:
                    self._style_menu.new_print("Not logged in")
                else:
                    self._style_menu.new_print("Application Menu.")
                    self._style_menu.new_print("1. To-do application.")
                    self._style_menu.new_print("2. Contacts.")
                    self._style_menu.new_print("3. Calculator applicaion.")
                    self._style_menu.new_print("4. Weather application.")
                    self._style_menu.new_print("5. Rate application.")
                    self._style_menu.new_print("6. Return to main menu.")
                    app_choice = input("Enter your choice: ")
                    if app_choice == "1":
                        todo = ToDoApp(self.current_id, self.current_email, self._style_menu)
                        todo.todo_app_menu()
                    elif app_choice == "2":
                        contact = Contacts(self.current_id, self._style_menu)
                        contact.contact_app_menu()
                    elif app_choice == "3":
                        calculator = Calculator(self._style_menu)
                        calculator.calculator_app_menu()
                    elif app_choice == "4":
                        weather = WeatherForecast("629c11a02db0490f99d123751240704", self._style_menu)
                        weather.weather_app_menu()
                    elif app_choice == "5":
                        rate = Rate(self._style_menu)
                        rate.rate_app_menu()
                    elif app_choice == "6":
                        continue
                    else:
                        self._style_menu.new_print("Invalid input")
            elif choice == "6":
                self.account_settings_menu()
            elif choice == "7":
                self._style_menu.style_settings_menu()
            elif choice == "8":
                self._style_menu.new_print("Exiting the program.")
                break
            else:
                self._style_menu.new_print("Invalid input. Please select an action again.")


if __name__ == "__main__":
    manager = AccountManager()
    manager.main()

