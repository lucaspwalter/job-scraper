import os
import smtplib
from email.message import EmailMessage

import requests
from dotenv import load_dotenv

from app.models.job import Job


load_dotenv()


def notify_job(job: Job) -> bool:
    try:
        email_sent = send_email(job)
    except (OSError, smtplib.SMTPException):
        email_sent = False

    send_whatsapp_if_configured(job)
    return email_sent


def send_email(job: Job) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    notify_email = os.getenv("NOTIFY_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, notify_email]):
        return False

    company = job.company or "Empresa nao informada"
    message = EmailMessage()
    message["Subject"] = f"Nova vaga encontrada: {job.title}"
    message["From"] = smtp_user
    message["To"] = notify_email
    message.set_content(f"Titulo: {job.title}\nEmpresa: {company}\nLink: {job.url}\n")

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(message)

    return True


def send_whatsapp_if_configured(job: Job) -> None:
    api_url = os.getenv("EVOLUTION_API_URL")
    api_key = os.getenv("EVOLUTION_API_KEY")
    instance = os.getenv("EVOLUTION_INSTANCE")
    phone = os.getenv("NOTIFY_PHONE")

    if not all([api_url, api_key, instance, phone]):
        return

    payload = {
        "number": phone,
        "text": (
            f"Nova vaga encontrada\n"
            f"Titulo: {job.title}\n"
            f"Empresa: {job.company or 'Empresa nao informada'}\n"
            f"Link: {job.url}"
        ),
    }
    headers = {"apikey": api_key, "Content-Type": "application/json"}
    endpoint = f"{api_url.rstrip('/')}/message/sendText/{instance}"

    try:
        requests.post(endpoint, json=payload, headers=headers, timeout=15).raise_for_status()
    except requests.RequestException:
        return
