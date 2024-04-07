import requests
from tabulate import tabulate

class WeatherForecast:
    def __init__(self, api_key):
        self.api_key = api_key

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

    def display_forecast(self, format_choice, city, days=3):
        forecast_info = self.get_forecast(city, days)
        if isinstance(forecast_info, list):
            headers = ["Date", "Max Temperature", "Min Temperature", "Weather Condition"]
            return tabulate(forecast_info, headers=headers, tablefmt=format_choice)
        else:
            return forecast_info
        


