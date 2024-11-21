from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv()


def send_email(mess):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    
    email = [
        "wangbosh0604@gmail.com",
            ]

    for receiver_email in email:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = (
            "[Notification from NYCU signin robot] Your signin status"
        )

        body = (mess)
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(sender_email, password)
                text = message.as_string()
                smtp.sendmail(sender_email, receiver_email, text)
                print(f"Email sent successfully to {receiver_email}!")
            except Exception as e:
                print(f"Failed to send email. Error: {e}")
                
                
                
