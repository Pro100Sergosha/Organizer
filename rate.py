import requests
from styles import Styles
class Rate:
    def __init__(self, style_menu = Styles()):
        self.style_menu = style_menu


    # Fetch currency information from the URL
    def get_currency_info(self, currency_code):
        try:
            response = requests.get("https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json/?date=2024-03-31")
            data = response.json()
            currencies = data[0]["currencies"]
            for currency in currencies:
                if currency['code'] == currency_code:
                    return currency
            return None
        except requests.RequestException:
            self.style_menu.new_print("Error fetching data")
            return None
        

    # Convert from GEL to another currency
    def gel_to_currency(self):
        while True:
            currency_code = input("Enter the currency code: ").upper()
            # Validate currency code
            if not self.validate_currency_code(currency_code):
                self.style_menu.new_print("Invalid currency code. Please enter a valid 3-character currency code.")
                continue
            amount_gel = input("Enter the amount in GEL: ")
            # Validate amount
            if not self.is_numeric(amount_gel):
                self.style_menu.new_print("Invalid amount. Please enter a valid numeric amount.")
                continue
            else:
                amount_gel = float(amount_gel)
                break
            
        currency_info = self.get_currency_info(currency_code)
        
        if currency_info:
            rate = currency_info['rate']
            quantity = currency_info['quantity']
            converted_amount = amount_gel / (rate * quantity)
            converted_amount_rounded = round(converted_amount, 2)
            self.style_menu.new_print(f"{amount_gel} GEL is approximately {converted_amount_rounded} {currency_info['code']}")
        else:
            self.style_menu.new_print("Failed to retrieve currency information. Please enter a valid currency code.")

    # Convert from another currency to GEL
    def currency_to_gel(self):
        while True:
            currency_code = input("Enter the currency code: ").upper()
            # Validate currency code
            if not self.validate_currency_code(currency_code):
                print("Invalid currency code. Please enter a valid 3-character currency code.")
                continue
            amount_currency = input("Enter the amount in the specified currency: ")
            # Validate amount
            if not self.is_numeric(amount_currency):
                self.style_menu.new_print("Invalid amount. Please enter a valid numeric amount.")
                continue
            else:
                amount_currency = float(amount_currency)
            
            currency_info = self.get_currency_info(currency_code)
            
            if currency_info:
                rate = currency_info['rate']
                quantity = currency_info['quantity']
                total = rate * quantity * amount_currency
                total_rounded = round(total, 2)
                self.style_menu.new_print(f"{amount_currency} {currency_info['code']} is approximately {total_rounded} GEL\n")
            else:
                self.style_menu.new_print("Failed to retrieve currency information. Please enter a valid currency code.")

    # Validate if the currency code exists in the URL data
    def validate_currency_code(self, currency_code):
        currency_info = self.get_currency_info(currency_code)
        return currency_info is not None

    

    # Check if a string can be converted to a float
    def is_numeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def rate_app_menu(self):
        while True:
            self.style_menu.new_print("1. Convert from GEL to currency")
            self.style_menu.new_print("2. Convert from Currency to GEL")
            self.style_menu.new_print("3. Return to main menu")
            option = input("Enter your choice: ")
            if option == '1':
                self.gel_to_currency()
            elif option == '2':
                self.currency_to_gel()
            elif option == '3':
                break
            else:
                self.style_menu.new_print("Invalid option. Please enter '1' or '2' or '3'.")

# Entry point of the program
if __name__ == "__main__":
    rate = Rate()
    rate.rate_app_menu()
