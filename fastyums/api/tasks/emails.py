from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_order_confirmation_email(order_id, email, full_name):
    """
    Send order confirmation mail to owner.
    """
    subject = "Oder Confirmation - FastYums"

    message = f"""
    Hi {full_name},

    Your order {order_id} has been successfully placed.

    Thanks for choosing FastYums.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
