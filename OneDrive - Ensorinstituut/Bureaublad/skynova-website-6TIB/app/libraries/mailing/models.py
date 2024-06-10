from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.libraries.mailing.settings import my_api_key,default_email

class emails:
    def send_no_reply_email(email,subject,html):
        message = Mail(
            from_email=default_email,
            to_emails=email,
            subject=subject,
            html_content=html
            )
        try:
            sg = SendGridAPIClient(my_api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)