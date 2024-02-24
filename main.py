import requests
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage


load_dotenv()
API_KEY = os.environ.get("API_KEY")
RECIPIENT_ADDR = os.environ.get("RECIPIENT_ADDR")
FROM_ADDR = os.environ.get("FROM_ADDR")
LOGIN = os.environ.get("LOGIN")
PASSWORD = os.environ.get("PASSWORD")
MAILHOST = os.environ.get("MAILHOST")
PORT = os.environ.get("PORT")
# This is the 3-hour (for max 5days) forecast API:
API_URL = "https://api.openweathermap.org/data/2.5/forecast"
PERIODS = 4  # 12 hours
params = {
    "lat": 47.258949,
    "lon": 8.848430,
    "appid": API_KEY,
    "cnt": PERIODS
}


def send_mail(email_addr, subject, content, bcc=None):
    print(f"Sending mail to {email_addr} from {FROM_ADDR}")

    with smtplib.SMTP(host=MAILHOST, port=PORT) as connection:
        connection.starttls()
        connection.login(LOGIN, PASSWORD)

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = FROM_ADDR
        msg["To"] = email_addr
        if bcc:
            msg["Bcc"] = bcc

        connection.send_message(msg)


response = requests.get(API_URL, params=params)
response.raise_for_status()
weather_data = response.json()

for hour_data in weather_data["list"]:
    condition = hour_data['weather'][0]['id']
    if condition < 700:
        will_rain = True

if will_rain:
    send_mail(RECIPIENT_ADDR, subject="Regenschirm mitnehmen!",
              content="Es wird heute regnen oder schneien...")
