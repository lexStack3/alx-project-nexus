from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from api.tasks.emails import send_order_confirmation_email


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        send_order_confirmation_email.delay(
            str(instance.order_id),
            instance.user.email,
            instance.user.full_name
        )
