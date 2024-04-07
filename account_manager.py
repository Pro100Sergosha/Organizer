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

        self.show_format = "simple"

        self.background = Back.RESET
        self.font_color = Fore.WHITE
        self.font_style = Style.NORMAL

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


    def show_accounts(self, format):
        self.check_file_exists(self.filename, self.fieldnames)
        with open(self.filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            accounts = []
            for row in reader:
                accounts.append([row["ID"], row["Nickname"], row["Email"]])
            return tabulate(accounts, headers=["ID", "Nickname", "Email", "Password"], tablefmt = format)


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
            self.new_print("Wrong password or email")

        return False

    def logout(self):
        self.logged_in = False
        self.current_email = None

    

    def change_password(self):
        if not self.logged_in:
            self.new_print=("You need to log in to change your password.")
            return

        new_password = input("Enter your new password: ")
        if not self.validate_password(new_password):
            self.new_print("Password must contain at least 8 characters, including one digit and one special character.")
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
        self.new_print("Password successfully updated.")

    def change_email(self):
        if not self.logged_in:
            self.new_print("You need to log in to change your email.")
            return

        new_email = input("Enter your new email: ")
        if not self.validate_email(new_email):
            self.new_print("Invalid Email format.")
            return

        if self.email_exists(new_email):
            self.new_print("User with this Email already exists.")
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
        self.new_print("Email successfully updated.")

    def change_nickname(self):
        if not self.logged_in:
            self.new_print("You need to log in to change your nickname.")
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
        self.new_print("Nickname successfully updated.")


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
        self.new_print("Account deleted.")
    



    def demo_show(self, format):
        demo_show = [["Demo First Name", "Demo Last Name", "Demo Email"]]
        return tabulate(demo_show, headers=["Header Name", "Header Last Name", "Header Email"], tablefmt = format)


    def font_style_menu(self):
        while True:
            print( Style.BRIGHT + "1. Bright font")
            print( Style.DIM + "2. Dim font")
            print( Style.NORMAL + "3. Normal font")
            print( Style.RESET_ALL + "4. Reset all font style settings")
            print("5. Return")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.font_style = Style.BRIGHT
            elif choice == "2":
                self.font_style = Style.DIM
            elif choice == "3":
                self.font_style = Style.NORMAL
            elif choice == "4":
                self.font_style = Style.RESET_ALL
            elif choice == "5":
                return
            else:
                print("Invalid input")

    def font_color_menu(self):
        while True:
            print( Fore.BLACK + "1. Black font")
            print( Fore.RED + "2. Red font")
            print( Fore.GREEN + "3. Green font")
            print( Fore.YELLOW + "4. Yellow font")
            print( Fore.BLUE + "5. Blue font")
            print( Fore.MAGENTA + "6. Magenta font")
            print( Fore.CYAN + "7. Cyan font")
            print( Fore.WHITE + "8. White font")
            print("9. Return")
            choice = input("Enter a number of color to change: ")
            if choice == "1":
                self.font_color = Fore.BLACK
            elif choice == "2":
                self.font_color = Fore.RED
            elif choice == "3":
                self.font_color = Fore.GREEN
            elif choice == "4":
                self.font_color = Fore.YELLOW
            elif choice == "5":
                self.font_color = Fore.BLUE
            elif choice == "6":
                self.font_color = Fore.MAGENTA
            elif choice == "7":
                self.font_color = Fore.CYAN
            elif choice == "8":
                self.font_color = Fore.WHITE
            elif choice == "9":
                return 
            else:
                print("Неверный выбор")

    def background_menu(self):
        while True:
            print(Back.BLACK + "1. Black background")
            print(Back.RED + "2. Red background")
            print(Back.GREEN + "3. Green background")
            print(Back.YELLOW + "4. Yellow background")
            print(Back.BLUE + "5. Blue background")
            print(Back.MAGENTA + "6. Magenta background")
            print(Back.CYAN + "7. Cyan background")
            print(Back.WHITE + "8. White background")
            print("9. Return to previus menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.background = Back.BLACK
            elif choice == "2":
                self.background = Back.RED
            elif choice == "3":
                self.background = Back.GREEN
            elif choice == "4":
                self.background = Back.YELLOW
            elif choice == "5":
                self.background = Back.BLUE
            elif choice == "6":
                self.background = Back.MAGENTA
            elif choice == "7":
                self.background = Back.CYAN
            elif choice == "8":
                self.background = Back.WHITE
            elif choice == "9":
                return 
            else:
                print("Invalid input")
        
    def list_style_menu(self):
        while True:
            print()
            print("1. Plain")
            print("2. Simple")
            print("3. Grid")
            print("4. Pipe")
            print("5. Orgtbl")
            print("6. Rst")
            print("7. Mediawiki")
            print("8. Html")
            print("9. Latex")
            print("10. Return to previus menu")
            format_choice = input("Enter a number of the format to try or\nEnter the name of format to change: ").lower()
            print()
            if format_choice == "1":
                print(self.demo_show("plain"))
            elif format_choice == "2":
                print(self.demo_show("simple"))
            elif format_choice == "3":
                print(self.demo_show("grid"))
            elif format_choice == "4":
                print(self.demo_show("pipe"))
            elif format_choice == "5":
                print(self.demo_show("orgtbl"))
            elif format_choice == "6":
                print(self.demo_show("rst"))
            elif format_choice == "7":
                print(self.demo_show("mediawiki"))
            elif format_choice == "8":
                print(self.demo_show("html"))
            elif format_choice == "9":
                print(self.demo_show("latex"))
            elif format_choice == "10":
                return
            elif format_choice in ["plain", "simple", "grid", "pipe", "orgtbl", "rst", "mediawiki", "html", "latex"]:
                self.list_format = format_choice
            else:
                print("Invalid input.")

    def style_settings_menu(self):
        print("1. Font color menu ")
        print("2. Font style menu ")
        print("3. Background menu")
        print("4. List style menu")
        print("5. Reset all styles")
        print("6. Return to previus menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            self.font_color_menu()
        elif choice == "2":
            self.font_style_menu()
        elif choice == "3":
            self.background_menu()
        elif choice == "4":
            self.list_style_menu()
        elif choice == "5":
            self.font_style = Style.RESET_ALL
            self.list_format = "plain"
        elif choice == "6":
            return 
        else:
            print("Invalid input")





    def new_print(self, text):
        return print(self.font_color + self.background + self.font_style + f"{text}")

    



    def account_settings_menu(self):
        if self.logged_in:
            self.new_print("\nSettings")
            self.new_print("1. Change nickname")
            self.new_print("2. Change password")
            self.new_print("3. Change email")
            self.new_print("4. Change list format")
            self.new_print("5. Delete account")
            self.new_print("6. Return to the main menu")
            setting_choice = input("Select an action: ")
            if setting_choice == "1":
                self.change_nickname()
            elif setting_choice == "2":
                self.change_password()
            elif setting_choice == "3":
                self.change_email()
            elif setting_choice == "4":
                self.list_settings_menu()
            elif setting_choice == "5":
                password = input("Enter your password: ")
                rewrite_password = input("Rewrite your password: ")
                current_password = self.account(self.current_id)['Password']
                if password == rewrite_password and bcrypt.checkpw(password.encode('utf-8'), current_password.encode('utf-8')):
                    self.delete_account(self.current_email)
                else:
                    self.new_print("Email does not exist")
            elif setting_choice == "6":
                self.new_print("Returning to the main menu")
            else:
                self.new_print("Invalid input. Please select an action again.")
        else:
            self.new_print("You need to log in to access settings.")

    
    def todo_app_menu(self):
        if self.current_id == None:
            self.new_print("You need to be logged in to access To-do application")
            return False
        else:
            self.todo_app = ToDoApp(self.current_id)
            self.new_print(f"Logged in as {self.current_email}")
        while True:
            self.new_print("\nTask Management Menu")
            self.new_print("1. Add a task")
            self.new_print("2. Mark a task as completed")
            self.new_print("3. Show all tasks")
            self.new_print("4. Delete a task")
            self.new_print("5. Return to main menu")

            choice = input("Choose an action: ")

            if choice == "1":
                list_tasks = []
                while True:
                    task = input("Enter the task or press ENTER to finish: ").strip()
                    if task == "":
                        for task in list_tasks:
                            self.todo_app.save_task(task)
                        self.new_print(self.todo_app.show_tasks())
                        break
                    else:
                        list_tasks.append(task)
            elif choice == "2":
                if not self.todo_app.file_exists():
                    self.new_print("You need to add task first!")
                else:
                    self.new_print(self.todo_app.show_tasks())
                    task_id = input("Enter the task ID to mark as completed: ")
                    self.todo_app.mark_task_completed(task_id)
            elif choice == "3":
                if not self.todo_app.file_exists():
                    self.new_print("You need to write your task first!")
                else:
                    self.new_print(self.todo_app.show_tasks(self.show_format))
            elif choice == "4":
                task_id = input("Enter the task ID to delete: ").strip()
                if not self.todo_app.file_exists():
                    self.new_print("You need to write your task first!")
                elif task_id == "":    
                    self.new_print("Task ID not found")
                else:
                    self.todo_app.delete_task(task_id)
            elif choice == "5":
                self.new_print("Returning to the main menu.")
                break
            else:
                self.new_print("Invalid input. Please choose an action again.")


    def contact_app_menu(self):
        contacts_manager = Contacts(self.current_id)
        while True:
            self.new_print("1. Add contact.")
            self.new_print("2. Show contacts.")
            self.new_print("3. Find contact.")
            self.new_print("4. Delete contact.")
            self.new_print("5. Return to main menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                phone_number = input("Enter phone number: ")
                email = input("Enter email: ").lower()
                contacts_manager.save_contact(first_name, last_name, phone_number, email)

            elif choice == "2":
                self.new_print(contacts_manager.show_contacts(self.show_format))

            elif choice == "3":
                contact = input("Find contact: ")
                self.new_print(contacts_manager.find_contact(contact))
            elif choice == "4":
                self.new_print(contacts_manager.show_contacts(self.show_format))
                contact_id = input("Enter ID of the contact to delete: ")
                contacts_manager.delete_contact(contact_id)
            elif choice == "5":
                break
            else:
                self.new_print("Invalid choice. Please enter a valid option.")


    def calculator_app_menu(self):
        calculator = Calculator()
        while True:
            expression = input("Enter an expression: ")

            # Validate input
            if not calculator.is_valid_expression(expression):
                print("Invalid expression. Please enter a valid expression.")
                continue

            # Check for square root or square operation
            if 'sqrt' in expression:
                result = calculator.calculate_sqrt(expression)
                if result is not None:
                    print("Result:", result)
            elif 'square' in expression:
                result = calculator.calculate_square(expression)
                if result is not None:
                    print("Result:", result)
            else:
                # Split the expression into operands and operator
                operator = calculator.get_operator(expression)
                num1, num2 = map(float, expression.split(operator))

                # Perform calculation based on operator
                if operator == '+':
                    print("Result:", calculator.add(num1, num2))
                elif operator == '-':
                    print("Result:", calculator.subtract(num1, num2))
                elif operator == '*':
                    print("Result:", calculator.multiply(num1, num2))
                elif operator == '/':
                    print("Result:", calculator.divide(num1, num2))
                elif operator == '%':
                    print("Result:", calculator.percent(num1, num2))

            print("1. Perform another calculation.")
            print()
            again = input("Do you want to perform another calculation? (yes/no): ")
            if again.lower() != 'yes':
                return


    def weather_app_menu(self):
        api_key = "629c11a02db0490f99d123751240704"
        weather = WeatherForecast(api_key)
        while True:
            print("1. See weather")
            print("2. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                city = input("Enter the city : ")
                days = int(input("Enter the number of days for forecast (maximum 10): "))
                if days > 10:
                    self.new_print("Maximum number of forecast days is 10.")
                self.new_print(weather.display_forecast(self.show_format,city, days))
            elif choice == "2":
                return
            else:
                print("Invalid input.")
            
            

    def main(self):
        while True:
            if self.current_email == None:
                self.new_print("Not logged in")
            else:
                self.new_print(f"Logged in as {self.current_email}")
            self.new_print("\nMain menu")
            self.new_print("1. Register a new account")
            self.new_print("2. Show the list of accounts")
            self.new_print("3. Log in")
            self.new_print("4. Logout")
            self.new_print("5. Applications")
            self.new_print("6. Account Settings")
            self.new_print("7. Style Settings")
            self.new_print("8. Exit")   
            choice = input("Enter your choice: ")    
            if choice == "1":
                nickname = input("Enter your Nickname: ")
                if nickname == "":
                    self.new_print("Nickname must be filled in.")
                    continue
                elif len(nickname) < 3:
                    self.new_print("Nickname length must be more than 3 characters.")
                    continue
                else:
                    email = input("Enter your Email: ").lower()
                    if not self.validate_email(email):
                        self.new_print("Invalid Email format.")
                        continue
                    password = input("Enter your password: ")
                    rewrite_password = input("Rewrite your password: ")
                    if not self.validate_password(password):
                        self.new_print("Password must contain at least 8 characters, including one digit and one special character.")
                        continue
                    elif password != rewrite_password:
                        self.new_print("Passwords must match")
                        continue
                    self.save_account(nickname, email, password)
            elif choice == "2":
                self.new_print(self.show_accounts(self.show_format))
            elif choice == "3":
                email = input("Enter your Email: ")
                password = input("Enter your password: ")
                self.login(email, password)
            elif choice == "4":
                self.logout()
            elif choice == "5":
                if self.current_email == None:
                    self.new_print("Not logged in")
                else:
                    self.new_print("Application Menu.")
                    self.new_print("1. To-do application.")
                    self.new_print("2. Contacts.")
                    self.new_print("3. Calculator applicaion.")
                    self.new_print("4. Weather application.")
                    self.new_print("5. Return to main menu")
                    app_choice = input("Enter your choice: ")
                    if app_choice == "1":
                        self.todo_app_menu()
                    elif app_choice == "2":
                        self.contact_app_menu()
                    elif app_choice == "3":
                        self.calculator_app_menu()
                    elif app_choice == "4":
                        self.weather_app_menu()
                    elif app_choice == "5":
                        continue
            elif choice == "6":
                self.account_settings_menu()
            elif choice == "7":
                self.style_settings_menu()
            elif choice == "8":
                self.new_print("Exiting the program.")
                break
            else:
                self.new_print("Invalid input. Please select an action again.")

if __name__ == "__main__":
    manager = AccountManager()
    manager.main()

