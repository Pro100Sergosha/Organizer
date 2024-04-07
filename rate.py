import requests

class Rate:
        

    # Here we have code, which is responsible for user typing GEL and getting amount in different currency
    def gel_to_currency(self):
        while True:
            currency_code = input("Enter the currency code: ").upper()
            if not currency_code.isalpha() or len(currency_code) != 3:
                print("Invalid currency code. Please enter a valid 3-character currency code.")
                continue
            amount_gel = input("Enter the amount in GEL: ")
            if not amount_gel.isdigit() and not self.is_float(amount_gel):
                print("Invalid amount. Please enter a valid numeric amount.")
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
            print(f"{amount_gel} GEL is approximately {converted_amount_rounded} {currency_info['code']}")
        else:
            print("Failed to retrieve currency information. Please enter a valid currency code.")

    # Here we have code, which is responsible for user typing currency and getting amount in GEL
    def currency_to_gel(self):
        while True:
            currency_code = input("Enter the currency code: ").upper()
            if not currency_code.isalpha() or len(currency_code) != 3:
                print("Invalid currency code. Please enter a valid 3-character currency code.")
                continue
            amount_currency = input("Enter the amount in the specified currency: ")
            if not amount_currency.isdigit() and not self.is_float(amount_currency):
                print("Invalid amount. Please enter a valid numeric amount.")
                continue
            else:
                amount_currency = float(amount_currency)
                break
            
        currency_info = self.get_currency_info(currency_code)
        
        if currency_info:
            rate = currency_info['rate']
            quantity = currency_info['quantity']
            total = rate * quantity * amount_currency
            total_rounded = round(total, 2)
            print(f"{amount_currency} {currency_info['code']} is approximately {total_rounded} GEL")
        else:
            print("Failed to retrieve currency information. Please enter a valid currency code.")


    # Here we are getting information from url:
    def get_currency_info(self,currency_code):
        try:
            response = requests.get("https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json/?date=2024-03-31")
            data = response.json()
            currencies = data[0]["currencies"]
            for currency in currencies:
                if currency['code'] == currency_code:
                    return currency
            return None
        except requests.RequestException:
            print("Error fetching data")
            return None

    def is_float(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        


## უკან გამოსვლის ფუნქციონალი აკლია და ეგ მგონი სხვებსაც ჭირდება და ყველას ერთი და იგივე ფუნქცია გავუწეროთ