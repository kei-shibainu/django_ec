import os
from django.conf import settings
from django.core.mail import EmailMessage, get_connection

class EmailSender:

    def __init__(self, to_list, message) -> None:
        self.to_list = to_list
        self.message = message
    
    def send_message(self):
        subject = "ご購入ありがとうございます"
        recipient_list = self.to_list
        from_email = "onboarding@resend.dev"
        message = self.message

        try:
            with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=os.environ["RESEND_API_KEY"],
                use_tls=True,
                ) as connection:
                    email = EmailMessage(
                        subject=subject,
                        body=message,
                        to=recipient_list,
                        from_email=from_email,
                        connection=connection).send()
        except Exception as e:
            raise e