import requests

# Here we are giving a choice to user, which operation is needed
def main():
    option = input("Enter '1' to convert from GEL to currency or '2' to convert from currency to GEL: ")
    if option == '1':
        gel_to_currency()
    elif option == '2':
        currency_to_gel()
    else:
        print("Invalid option. Please enter '1' or '2'.")

# Here we have code, which is responsible for user typing GEL and getting amount in different currency
def gel_to_currency():
    currency_code = input("Enter the currency code: ").upper()
    amount_gel = float(input("Enter the amount in GEL: "))
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
    currency_code = input("Enter the currency code: ").upper()
    amount_currency = float(input("Enter the amount in the specified currency: "))
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
    
if __name__ == "__main__":
    main()
