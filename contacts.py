import csv
import os
from tabulate import tabulate
from styles import Styles

class Contacts:
    def __init__(self, user_id = None, style_menu = Styles()):
        self.user_id = user_id
        self.style_menu = style_menu
        self.file_path = f"{user_id}'s_contacts.csv"
        self.fieldnames = ["ID", "First Name", "Last Name", "Phone Number", "Email"]
        self.current_directory = os.path.dirname(__file__)
        self.contacts_folder = os.path.join(self.current_directory, 'Contacts')
        self.file_path = os.path.join(self.contacts_folder, self.file_path)

    def save_contact(self, first_name, last_name, phone_number, email):
        if not os.path.exists(self.contacts_folder):
            os.makedirs(self.contacts_folder)

        contact_id = 0
        if os.path.exists(self.file_path) and os.stat(self.file_path).st_size != 0:
            with open(self.file_path, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                ids = [int(row["ID"]) for row in reader]
                contact_id = len(ids) + 1
        else:
            with open(self.file_path, "w") as file:
                contact_id = 1

        with open(self.file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if os.stat(self.file_path).st_size == 0:
                writer.writeheader()
            writer.writerow({"ID": contact_id, "First Name": first_name, "Last Name": last_name, "Phone Number": phone_number, "Email": email})
            print("Contact successfully added.")


    def file_exists(self):
        return os.path.exists(self.file_path)


    def list_contacts(self):
        with open(self.file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = []
            contacts.extend(contact for contact in reader)
            return list(contacts)

    def check_file_exists(self, filename, fieldnames):
        if not os.path.exists(filename):
            with open(filename, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def show_contacts(self):
        self.check_file_exists(self.file_path, self.fieldnames)
        contacts = self.list_contacts()
        new_contacts = []
        for contact in contacts:
            new_contacts.append([contact["ID"], contact["First Name"], contact["Last Name"], contact["Phone Number"], contact["Email"]])
        return tabulate(new_contacts, headers=["ID", "First Name", "Last Name", "Phone Number", "Email"], tablefmt = self.style_menu.list_format())


    def check_contact(self, contact_id):
        contacts = self.list_contacts()
        contact_exists = any(contact["ID"] == contact_id for contact in contacts)
        return contact_exists


    def delete_contact(self, contact_id):
        contacts = self.list_contacts()
        if not self.check_contact(contact_id):
            print(f"Contact with this ID not found.")
            return
        else:
            with open(self.file_path, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()
                for contact in contacts:
                    if contact["ID"] == contact_id:
                        contacts.remove(contact)
                writer.writerows(contacts)
            print(f"Contact deleted.")


    def find_contact(self, contact_input):
        new_contacts = []
        contacts = self.list_contacts()
        for contact in contacts:
            if contact_input in [contact["ID"], contact["First Name"], contact["Last Name"], contact["Phone Number"], contact["Email"]]:
                new_contacts.append([contact["ID"], contact["First Name"], contact["Last Name"], contact["Phone Number"], contact["Email"]])

        if len(new_contacts) < 1:
            return "There is not such contact"
        else:        
            return tabulate(new_contacts, headers=["ID", "First Name", "Last Name", "Phone Number", "Email"])


    def contact_app_menu(self):
        while True:
            self.style_menu.new_print("1. Add contact.")
            self.style_menu.new_print("2. Show contacts.")
            self.style_menu.new_print("3. Find contact.")
            self.style_menu.new_print("4. Delete contact.")
            self.style_menu.new_print("5. Return to main menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                phone_number = input("Enter phone number: ")
                email = input("Enter email: ").lower()
                self.save_contact(first_name, last_name, phone_number, email)

            elif choice == "2":
                self.style_menu.new_print(self.show_contacts())

            elif choice == "3":
                contact = input("Find contact: ")
                self.style_menu.new_print(self.find_contact(contact))
            elif choice == "4":
                self.style_menu.new_print(self.show_contacts())
                contact_id = input("Enter ID of the contact to delete: ")
                self.delete_contact(contact_id)
            elif choice == "5":
                break
            else:
                self.style_menu.new_print("Invalid choice. Please enter a valid option.")



if __name__ == "__main__":
    contact_manager = Contacts()
