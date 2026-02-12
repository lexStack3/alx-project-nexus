from django.db.models.signals import pre_save
from django.dispatch import receiver
from payments.models import Payment
from api.tasks.payment_emails import send_payment_success_email


@receiver(pre_save, sender=Payment)
def payment_status_change_handler(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        previous = Payment.objects.get(pk=instance.pk)
    except Payment.DoesNotExist:
        return

    if previous.status != instance.status:
        if instance.status == Payment.PaymentStatus.SUCCESSFUL:
            send_payment_success_email.delay(
                str(instance.payment_id),
                instance.user.email,
                instance.user.full_name,
                str(instance.amount)
            )
    return
