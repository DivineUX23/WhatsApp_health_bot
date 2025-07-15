from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
from_number = os.getenv("FROM")

client = Client(account_sid, auth_token)
def send_message(to: str, message: str) -> None:

    send = client.messages.create(
        from_=f"whatsapp:{from_number}",
        body=message,
        to=to
    )

    #print(f"by whatsapp {send}")