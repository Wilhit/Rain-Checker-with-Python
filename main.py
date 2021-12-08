import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

LON = 17.0832
LAT = -22.5594

# https://api.openweathermap.org/
# Get the api_key, account_sid, auth_token from the website above

api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

account_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

parameters = {
    'lat': LAT,
    'lon': LON,
    'appid': api_key,
    'exclude': 'current,minutely,daily'
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
# weather_data["hourly"]
weather_slice = weather_data["hourly"][:12]

will_rain = False
for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]['id'])
    if condition_code < 700:
        will_rain =True


if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="\n\nIt's going to rain today. Remember to bring an Umbrella, and remember to smile.\n\nI love you, Asvia",
        from_='+18507717404',
        to='+264816345342',
    )
    print(message.sid)

else:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="\n\nNo chances of raining today. Have a good day and remember to always smile.\n\nI love you, Asvia",
        from_='+18507717404',
        to='+264812702607',
    )
    print(message.sid)

# print(weather_slice)
# print(weather_data["hourly"][0]['weather'][0])
# print(weather_data)

