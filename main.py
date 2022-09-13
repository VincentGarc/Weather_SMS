import requests
import os
from twilio.rest import Client
from decouple import config

account_sid = config('ACC_SID')
auth_token = config('AUTH_TOKEN')
client = Client(account_sid, auth_token)
will_rain: bool = False
weather_params = {
    "lat": config('LAT'),
    "lon": config('LON'),
    "appid": config('API_KEY'),
    "exclude": "current,minutely,daily"
}

OWM_Endpoint: str = "https://api.openweathermap.org/data/2.5/onecall"

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔",
        from_=config('TEL_TWILIO'),
        to=config('RECIPIENT')
    )

    print(message.status)
