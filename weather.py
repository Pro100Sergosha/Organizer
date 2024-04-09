import requests
from tabulate import tabulate
from styles import Styles





class WeatherForecast():
    def __init__(self, api_key, style_menu = Styles()):
        self.api_key = api_key
        self.style_menu = style_menu
    def get_forecast(self, city, days=3):
        url = f"http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&days={days}&lang=en"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            forecast = data['forecast']['forecastday']
            forecast_info = []
            for day in forecast:
                date = day['date']
                max_temp_c = day['day']['maxtemp_c']
                min_temp_c = day['day']['mintemp_c']
                condition = day['day']['condition']['text']
                forecast_info.append([date, f"{max_temp_c}°C", f"{min_temp_c}°C", condition])
            return forecast_info
        else:
            f"Failed to get weather forecast. Error code: {response.status_code}"

    def display_forecast(self, city, days=3):
        forecast_info = self.get_forecast(city, days)
        if isinstance(forecast_info, list):
            headers = ["Date", "Max Temperature", "Min Temperature", "Weather Condition"]
            return tabulate(forecast_info, headers=headers, tablefmt=self.style_menu.list_format())
        else:
            return forecast_info
        
    def weather_app_menu(self):
        while True:
            try:
                self.style_menu.new_print("1. See weather")
                self.style_menu.new_print("2. Return to main menu")
                choice = input("Enter your choice: ")
                if choice == "1":
                    city = input("Enter the city: ")
                    days = int(input("Enter the number of days for forecast (maximum 10): "))

                    if days > 10:
                        self.style_menu.new_print("Maximum number of forecast days is 10.")
                    self.style_menu.new_print(self.display_forecast(city, days))
                elif choice == "2":
                    return
                else:
                    self.style_menu.new_print("Invalid input.")
            except ValueError:
                self.style_menu.new_print("Invalid input.")


if __name__ == "__main__":
    weater = WeatherForecast("629c11a02db0490f99d123751240704")
    weater.weather_app_menu()