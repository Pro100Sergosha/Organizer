import csv
import os
import re
import bcrypt
from tabulate import tabulate
from to_do_app import ToDoApp

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
                next_id = max(ids) + 1

        hashed_password = self.hash_password(password)

        
        with open(self.filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if os.stat(self.filename).st_size == 0:
                writer.writeheader()
            writer.writerow({"ID": next_id, "Nickname": nickname, "Email": email, "Password": hashed_password.decode()})
            print("You've registered!\nYour id is: ", next_id)


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


    def show_accounts(self):
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            accounts = []
            for row in reader:
                accounts.append([row["ID"], row["Nickname"], row["Email"], row["Password"]])
            return tabulate(accounts, headers=["ID", "Nickname", "Email", "Password"])


    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


    def login(self, email, password):
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in list(reader):
                if row["Email"] == email and self.check_password(password, row["Password"]):
                    self.logged_in = True
                    self.current_email = email
                    self.current_id = row["ID"]
                    self.current_account = row
                    return True
            print("Wrong password or email")

        return False


    def logout(self):
        self.logged_in = False
        self.current_email = None


    def change_password(self):
        if not self.logged_in:
            print("You need to log in to change your password.")
            return

        new_password = input("Enter your new password: ")
        if not self.validate_password(new_password):
            print("Password must contain at least 8 characters, including one digit and one special character.")
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
        print("Password successfully updated.")


    def change_email(self):
        if not self.logged_in:
            print("You need to log in to change your email.")
            return

        new_email = input("Enter your new email: ")
        if not self.validate_email(new_email):
            print("Invalid Email format.")
            return

        if self.email_exists(new_email):
            print("User with this Email already exists.")
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
        print("Email successfully updated.")


    def change_nickname(self):
        if not self.logged_in:
            print("You need to log in to change your nickname.")
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
        print("Nickname successfully updated.")


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
        print("Account deleted.")
    

    def todo_app_menu(self):
        if self.current_id == None:
            print("You need to be logged in to access To-do application")
            return False
        else:
            self.todo_app = ToDoApp(self.current_id)
            print(f"Logged in as {self.current_email}")
        while True:
            print("\nTask Management Menu")
            print("1. Add a task")
            print("2. Mark a task as completed")
            print("3. Show all tasks")
            print("4. Delete a task")
            print("5. Return to main menu")

            choice = input("Choose an action: ")

            if choice == "1":
                task = input("Enter the task: ").strip()
                if task == "":
                    print("Task must be filled in")
                else:
                    self.todo_app.save_task(task)
            elif choice == "2":
                if not self.todo_app.file_exists():
                    print("You need to add task first!")
                else:
                    print(self.todo_app.show_tasks())
                    task_id = input("Enter the task ID to mark as completed: ")
                    self.todo_app.mark_task_completed(task_id)
            elif choice == "3":
                if not self.todo_app.file_exists():
                    print("You need to write your task first!")
                else:
                    print(self.todo_app.show_tasks())
            elif choice == "4":
                task_id = input("Enter the task ID to delete: ").strip()
                if not self.todo_app.file_exists():
                    print("You need to write your task first!")
                elif task_id == "":    
                    print("Task ID not found")
                else:
                    self.todo_app.delete_task(task_id)
            elif choice == "5":
                print("Returning to the main menu.")
                break
            else:
                print("Invalid input. Please choose an action again.")


    def main(self):
        while True:
            if self.current_email == None:
                print("Not logged in")
            else:
                print(f"Logged in as {self.current_email}")
            print("\nMain menu")
            print("1. Register a new account")
            print("2. Show the list of accounts")
            print("3. Log in")
            print("4. Logout")
            print("5. To-do application")
            print("6. Settings")
            print("7. Exit")

            choice = input("Select an action: ")

            if choice == "1":
                nickname = input("Enter your Nickname: ")
                if nickname == "":
                    print("Nickname must be filled in.")
                    continue
                elif len(nickname) < 3:
                    print("Nickname length must be more than 3 characters.")
                    continue
                else:
                    email = input("Enter your Email: ").lower()
                    if not self.validate_email(email):
                        print("Invalid Email format.")
                        continue
                    password = input("Enter your password: ")
                    rewrite_password = input("Rewrite your password: ")
                    if not self.validate_password(password):
                        print("Password must contain at least 8 characters, including one digit and one special character.")
                        continue
                    elif password != rewrite_password:
                        print("Passwords must match")
                        continue
                    self.save_account(nickname, email, password)
            elif choice == "2":
                print(self.show_accounts())
            elif choice == "3":
                email = input("Enter your Email: ")
                password = input("Enter your password: ")
                self.login(email, password)
            elif choice == "4":
                self.logout()
            elif choice == "5":
                self.todo_app_menu()
                
            elif choice == "6":
                if self.logged_in:
                    print("\nSettings")
                    print("1. Change nickname")
                    print("2. Change password")
                    print("3. Change email")
                    print("4. Delete account")
                    print("5. Return to the main menu")
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
                            print("Email does not exist")
                    elif setting_choice == "5":
                        print("Returnin to the main menu")
                    else:
                        print("Invalid input. Please select an action again.")
                else:
                    print("You need to log in to access settings.")
            elif choice == "7":
                print("Exiting the program.")
                break
            else:
                print("Invalid input. Please select an action again.")


if __name__ == "__main__":
    manager = AccountManager()
    manager.main()