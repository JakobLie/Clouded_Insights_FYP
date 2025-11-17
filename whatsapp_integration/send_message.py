from dotenv import load_dotenv
import os
import requests

load_dotenv()

WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# User must be sent this onboard message first, before any other messages
def send_whatsapp_onboard_message(to_number):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
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
def send_whatsapp_custom_message(phone_number, subject, body):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,      # single number
        "type": "text",
        "text": {"body": f"{subject}\n\n{body}"}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f" * WhatsApp message sent to {phone_number} successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {f" * Error sending WhatsApp message to {phone_number}: {e}"}

if __name__ == "__main__":
    message = "This is an automated message from NotificationBot of the CloudedInsights Business Account.\n\nNotifications regarding TSH's predicted PNL Performance will be sent via this conversation."
    send_whatsapp_custom_message(
        to_number = "6596694584", 
        subject = message)

# for number in phone_numbers:
#     result = send_whatsapp_custom_message(number, message)
#     print(number, result)