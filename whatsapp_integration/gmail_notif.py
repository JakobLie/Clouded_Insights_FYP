import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# METHOD
def sendEmailNotification(email, subject, body):
    message = MIMEMultipart()
    message["From"] = f"Traffic-light Simulation Hub <{SENDER_EMAIL}>"
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD) # Log in to Gmail account
            server.send_message(message) # Send the email
        print(f" * Email sent to {email} successfully")
    except Exception as e:
        print(f" * Failed to send email to {email}: {e}")

if __name__ == "__main__":
    sendEmailNotification(
        email = "jeremylin.2022@scis.smu.edu.sg", 
        subject = f"test email notif", 
        body = f"test test test 2")