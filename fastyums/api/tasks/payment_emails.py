from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_payment_success_email(self, payment_id, email, full_name, amount):
    try:
        subject = "Payment Successful - FastYums"

        message = f"""
        Hi {full_name}

        Your payment of ₦{amount} was successful.

        Thank you for shopping with FastYums.
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

    except Exception as exc:
        raise self.retry(exc=exc, countdown=3)
