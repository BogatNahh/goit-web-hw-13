from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText

SMTP_USER = "your@email.com"
SMTP_PASS = "yourpassword"

def send_verification_email(email: str, token: str, background_tasks: BackgroundTasks):
    verification_link = f"http://localhost:8000/auth/verify?token={token}"
    message = MIMEText(f"Перейдіть за посиланням для підтвердження email: {verification_link}")
    message["Subject"] = "Підтвердження реєстрації"
    message["From"] = SMTP_USER
    message["To"] = email

    def send_email():
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, email, message.as_string())

    background_tasks.add_task(send_email)
