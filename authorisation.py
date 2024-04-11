import re
import os
import csv
import bcrypt


class Authorisation:
        def __init__(self, style_menu, filename="accounts.csv"):
            self.filename = filename
            self.fieldnames = ["ID", "Nickname", "Email", "Password"]
            self._email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            self._password_regex = r"^(?=.*\d)(?=.*[!@#$%^&*()])(?=.*[a-zA-Z]).{8,}$"

            self._logged_in = False
            self._current_id = None
            self._current_email = None
            self._current_account = None
            self._current_nickname = None

            self._style_menu = style_menu


        def save_account(self, nickname, email, password):
            if not self.check_email(email):
                self._style_menu.new_print("Invalid Email format.")
                return

            if not self.check_password(password):
                self._style_menu.new_print("Password must contain at least 8 characters, including one digit and one special character.")
                return

            if not os.path.exists(self.filename):
                with open(self.filename, "w", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writeheader()

            with open(self.filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["Email"] == email:
                        self._style_menu.new_print("An account with this Email already exists.")
                        return

            next_id = 0

            if os.path.exists(self.filename) and os.stat(self.filename).st_size != 0:
                with open(self.filename, "r", newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    ids = [int(row["ID"]) for row in reader]
                    next_id = len(ids) + 1

            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())


            with open(self.filename, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                if os.stat(self.filename).st_size == 0:
                    writer.writeheader()
                writer.writerow({"ID": next_id, "Nickname": nickname, "Email": email, "Password": hashed_password.decode()})
                self._style_menu.new_print("You've registered!")


        def login(self, email, password):
            if not os.path.exists(self.filename):
                with open(self.filename, "w", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writeheader()

            with open(self.filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in list(reader):
                    if row["Email"] == email and bcrypt.checkpw(password.encode('utf-8'), row["Password"].encode('utf-8')):
                        self._logged_in = True
                        self._current_email = email
                        self._current_id = row["ID"]
                        self._current_account = row
                        self.logged_in()
                        return True
                self._style_menu.new_print("Wrong password or email")

            return False


        def logout(self):
            self._logged_in = False
            self._current_email = None
 
        def check_password(self, password):
            return re.match(self._password_regex, password)

        def check_email(self, mail):
            return re.match(self._email_regex, mail)

        def logged_in(self):
            return self._logged_in
        def current_id(self):
            return self._current_id
        def current_email(self):
            return self._current_email
        def current_account(self):
            return self._current_account
        def current_nickname(self):
            return self._current_nickname
        