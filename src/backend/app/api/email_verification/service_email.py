import smtplib
from email.message import EmailMessage

from app.settings import settings


def send_otp_email(to_email: str, otp: str) -> None:
    message = EmailMessage()
    message["Subject"] = "Verifikasi Email - Internal Business Strategic Platform"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message.set_content(
        f"""Halo,

Kode OTP untuk verifikasi email kamu adalah: {otp}

Kode ini berlaku selama 5 menit.
Jangan bagikan kode ini kepada siapa pun.

Jika kamu tidak merasa melakukan registrasi, abaikan email ini.
"""
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)