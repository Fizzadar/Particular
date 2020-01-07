import requests

from particular_admin.settings import (
    MAILGUN_API_KEY,
    MAILGUN_DOMAIN,
    MAILGUN_FROM_ADDRESS,
)


def send_email(to_emails, subject, text):
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    response = requests.post(
        f'https://api.eu.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
        auth=('api', MAILGUN_API_KEY),
        data={
            'from': MAILGUN_FROM_ADDRESS,
            'to': to_emails,
            'subject': subject,
            'text': text,
        },
    )
    response.raise_for_status()
