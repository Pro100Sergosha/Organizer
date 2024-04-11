import os
import csv
from tabulate import tabulate
class Menu:
    def __init__(self, style_menu):
        self._style_menu = style_menu


    def show_accounts(self):
        if not os.path.exists('accounts.csv'):
            with open('accounts.csv', "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames= ["ID", "Nickname", "Email", "Password"])
                writer.writeheader()
        with open('accounts.csv', "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            accounts = []
            for row in reader:
                accounts.append([row["ID"], row["Nickname"], row["Email"]])
            return tabulate(accounts, headers=["ID", "Nickname", "Email", "Password"], tablefmt = self._style_menu.list_format())
        
    def main_menu(self):
        self._style_menu.new_print("\nMain menu")
        self._style_menu.new_print("1. Register a new account")
        self._style_menu.new_print("2. Show the list of accounts")
        self._style_menu.new_print("3. Log in")
        self._style_menu.new_print("4. Logout")
        self._style_menu.new_print("5. Applications")
        self._style_menu.new_print("6. Account Settings")
        self._style_menu.new_print("7. Style Settings")
        self._style_menu.new_print("8. Exit")

    def app_menu(self):
        self._style_menu.new_print("\nApplication Menu.")
        self._style_menu.new_print("1. To-do application.")
        self._style_menu.new_print("2. Contacts.")
        self._style_menu.new_print("3. Calculator applicaion.")
        self._style_menu.new_print("4. Weather application.")
        self._style_menu.new_print("5. Rate application.")
        self._style_menu.new_print("6. Return to main menu.")