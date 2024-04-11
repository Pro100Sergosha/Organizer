from to_do_app import ToDoApp
from contacts import Contacts
from calculator import Calculator
from weather import WeatherForecast
from rate import Rate
from styles import Styles
from update_account import Update
from menus import Menu
from authorisation import Authorisation



def main(): 
    style_menu = Styles()
    manager = Authorisation(style_menu)
    menu = Menu(style_menu)
    while True:
        if not manager.logged_in():
            style_menu.new_print("Not logged in")
        else:
            style_menu.new_print(f"Logged in as {manager.current_email()}")
        menu.main_menu()
        choice = input("Enter your choice: ")    
        if choice == "1":
            nickname = input("Enter your Nickname: ")
            if nickname == "":
                style_menu.new_print("Nickname must be filled in.")
                continue
            elif len(nickname) < 3:
                style_menu.new_print("Nickname length must be more than 3 characters.")
                continue
            else:
                email = input("Enter your Email: ").lower()
                if not manager.check_email():
                    style_menu.new_print("Invalid Email format.")
                    continue
                password = input("Enter your password: ")
                rewrite_password = input("Rewrite your password: ")
                if not manager.check_password():
                    style_menu.new_print("Password must contain at least 8 characters, including one digit and one special character.")
                    continue
                elif password != rewrite_password:
                    style_menu.new_print("Passwords must match")
                    continue
                manager.save_account(nickname, email, password)
        elif choice == "2":
            style_menu.new_print(menu.show_accounts())
        elif choice == "3":
            email = input("Enter your Email: ")
            password = input("Enter your password: ")
            manager.login(email, password)
        elif choice == "4":
            manager.logout()
        elif choice == "5":
            if manager.current_email() == None:
                style_menu.new_print("Not logged in")
            else:
                menu.app_menu()
                app_choice = input("Enter your choice: ")
                if app_choice == "1":
                    todo = ToDoApp(manager.current_id(), manager.current_email(), style_menu)
                    todo.todo_app_menu()
                elif app_choice == "2":
                    contact = Contacts(manager.current_id(), style_menu)
                    contact.contact_app_menu()
                elif app_choice == "3":
                    calculator = Calculator(style_menu)
                    calculator.calculator_app_menu()
                elif app_choice == "4":
                    weather = WeatherForecast("629c11a02db0490f99d123751240704", style_menu)
                    weather.weather_app_menu()
                elif app_choice == "5":
                    rate = Rate(style_menu)
                    rate.rate_app_menu()
                elif app_choice == "6":
                    continue
                else:
                    style_menu.new_print("Invalid input")
        elif choice == "6":
            account = Update(manager.current_email(), manager.logged_in(), style_menu)
            account.account_settings_menu()
        elif choice == "7":
            style_menu.style_settings_menu()
        elif choice == "8":
            style_menu.new_print("Exiting the program.")
            break
        else:
            style_menu.new_print("Invalid input. Please select an action again.")


if __name__ == "__main__":
    main()