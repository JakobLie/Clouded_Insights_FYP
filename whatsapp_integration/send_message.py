from dotenv import load_dotenv
import os
import requests

load_dotenv()

PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# User must be sent this onboard message first, before any other messages
def send_whatsapp_onboard_message(to_number):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,      # single number
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# User must have replied to onboard message within 24 hours to be able to receive custom message
def send_whatsapp_custom_message(to_number, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,      # single number
        "type": "text",
        "text": {"body": text}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

phone_numbers = ["6587654321", "6512345678"]
message = "This is an automated message from NotificationBot of the CloudedInsights Business Account.\n\nNotifications regarding TSH's predicted PNL Performance will be sent via this conversation."

print(send_whatsapp_custom_message("6596694584", message))

# for number in phone_numbers:
#     result = send_whatsapp_custom_message(number, message)
#     print(number, result)