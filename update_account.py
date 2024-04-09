import csv
import bcrypt
import re
from styles import Styles



class Update:
    def __init__(self, user_id = "1", logged_in = None , user_nickname = None, user_mail = None, user_password = None, style_menu = Styles()):
        self.logged_in = logged_in
        self.user_id = user_id
        self.user_nickname = user_nickname
        self.user_mail = user_mail
        self.user_password = user_password
        self.style_menu = style_menu

        self.email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.password_regex = r"^(?=.*\d)(?=.*[!@#$%^&*()])(?=.*[a-zA-Z]).{8,}$"

        self.fieldnames = ["ID", "Nickname", "Email", "Password"]

    def update_account_info(self, field_to_update, new_value):
        if not self.logged_in:
            self.style_menu.new_print("You need to log in to update your account information.")
            return

        accounts = []
        with open("accounts.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                accounts.append(row)

        updated_accounts = []
        for account in accounts:
            if account["Email"] == self.user_mail:
                account[field_to_update] = new_value
            updated_accounts.append(account)

        with open("accounts.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in updated_accounts:
                writer.writerow(account)

        if field_to_update == "Password":
            self.style_menu.new_print("Password successfully updated.")
        elif field_to_update == "Email":
            self.style_menu.new_print("Email successfully updated.")
        elif field_to_update == "Nickname":
            self.style_menu.new_print("Nickname successfully updated.")

    def change_password(self):
        new_password = input("Enter your new password: ")
        if not self.validate_password(new_password):
            self.style_menu.new_print("Password must contain at least 8 characters, including one digit and one special character.")
            return

        hashed_password = self.hash_password(new_password)
        self.update_account_info("Password", hashed_password.decode())

    def change_email(self):
        new_email = input("Enter your new email: ")
        if not self.validate_email(new_email):
            self.style_menu.new_print("Invalid Email format.")
            return

        if self.email_exists(new_email):
            self.style_menu.new_print("User with this Email already exists.")
            return

        self.update_account_info("Email", new_email)

    def email_exists(self, email):
        with open("accounts.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Email"] == email:
                    return True
        return False

    def change_nickname(self):
        new_nickname = input("Enter your new nickname: ")
        self.update_account_info("Nickname", new_nickname)

    def account(self):
        with open("accounts.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, val in row.items():
                    if val == self.user_id:
                        return row
            return
        
    def validate_password(self, password):
        return re.match(self.password_regex, password)
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_email(self, email):
        return re.match(self.email_regex, email)

    def delete_account(self, email):
        accounts = []
        with open("accounts.csv", "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Email"] != email:
                    accounts.append(row)

        with open("accounts.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for account in accounts:
                writer.writerow(account)
        self.current_email = None
        self.logged_in = False
        self.style_menu.new_print("Account deleted.")

    def account_settings_menu(self):
        if self.logged_in:
            self.style_menu.new_print("\nSettings")
            self.style_menu.new_print("1. Change nickname")
            self.style_menu.new_print("2. Change password")
            self.style_menu.new_print("3. Change email")
            self.style_menu.new_print("4. Delete account")
            self.style_menu.new_print("5. Return to the main menu")
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
                current_password = self.account()['Password']
                if password == rewrite_password and bcrypt.checkpw(password.encode('utf-8'), current_password.encode('utf-8')):
                    self.delete_account(self.current_email)
                else:
                    self.style_menu.new_print("Email does not exist")
            elif setting_choice == "5":
                self.style_menu.new_print("Returning to the main menu")
            else:
                self.style_menu.new_print("Invalid input. Please select an action again.")
        else:
            self.style_menu.new_print("You need to log in to access settings.")

if __name__ == "__main__":
    account = Update()
    account.account()