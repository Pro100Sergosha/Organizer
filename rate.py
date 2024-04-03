import requests

# Here we are giving a choice to user, which operation is needed
def main():
    while True:
        option = input("Enter '1' to convert from GEL to currency or '2' to convert from currency to GEL: ")
        if option == '1':
            gel_to_currency()
            break
        elif option == '2':
            currency_to_gel()
            break
        else:
            print("Invalid option. Please enter '1' or '2'.")

# Here we have code, which is responsible for user typing GEL and getting amount in different currency
def gel_to_currency():
    while True:
        currency_code = input("Enter the currency code: ").upper()
        if not currency_code.isalpha() or len(currency_code) != 3:
            print("Invalid currency code. Please enter a valid 3-character currency code.")
            continue
        amount_gel = input("Enter the amount in GEL: ")
        if not amount_gel.isdigit() and not is_float(amount_gel):
            print("Invalid amount. Please enter a valid numeric amount.")
            continue
        else:
            amount_gel = float(amount_gel)
            break
        
    currency_info = get_currency_info(currency_code)
    
    if currency_info:
        rate = currency_info['rate']
        quantity = currency_info['quantity']
        converted_amount = amount_gel / (rate * quantity)
        converted_amount_rounded = round(converted_amount, 2)
        print(f"{amount_gel} GEL is approximately {converted_amount_rounded} {currency_info['code']}")
    else:
        print("Failed to retrieve currency information. Please enter a valid currency code.")

# Here we have code, which is responsible for user typing currency and getting amount in GEL
def currency_to_gel():
    while True:
        currency_code = input("Enter the currency code: ").upper()
        if not currency_code.isalpha() or len(currency_code) != 3:
            print("Invalid currency code. Please enter a valid 3-character currency code.")
            continue
        amount_currency = input("Enter the amount in the specified currency: ")
        if not amount_currency.isdigit() and not is_float(amount_currency):
            print("Invalid amount. Please enter a valid numeric amount.")
            continue
        else:
            amount_currency = float(amount_currency)
            break
        
    currency_info = get_currency_info(currency_code)
    
    if currency_info:
        rate = currency_info['rate']
        quantity = currency_info['quantity']
        total = rate * quantity * amount_currency
        total_rounded = round(total, 2)
        print(f"{amount_currency} {currency_info['code']} is approximately {total_rounded} GEL")
    else:
        print("Failed to retrieve currency information. Please enter a valid currency code.")


# Here we are getting information from url:
def get_currency_info(currency_code):
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()

## უკან გამოსვლის ფუნქციონალი აკლია და ეგ მგონი სხვებსაც ჭირდება და ყველას ერთი და იგივე ფუნქცია გავუწეროთ