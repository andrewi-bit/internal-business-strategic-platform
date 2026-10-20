import smtplib
import ssl
from email.message import EmailMessage

from app.settings import settings

def send_password_reset_email(
    to_email: str,
    reset_url: str,
) -> None:
    message = EmailMessage()
    message["Subject"] = (
        "Reset Password - Internal Business Strategic Platform"
    )
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email

    message.set_content(
        f"""Halo,

Kami menerima permintaan untuk mereset password akun kamu.

Klik link berikut untuk membuat password baru:
{reset_url}

Link ini hanya berlaku selama 15 menit dan hanya dapat digunakan satu kali.

Jika kamu tidak meminta reset password, abaikan email ini.
Password kamu tidak akan berubah tanpa menyelesaikan proses reset.

Salam,
Internal Business Strategic Platform
"""
    )

    context = ssl.create_default_context()

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
    ) as server:
        server.starttls(context=context)
        server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
        )
        server.send_message(message)
