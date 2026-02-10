import uuid
from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from orders.models import Order


User = get_user_model()


class Payment(BaseModel):
    """
    A model representation of a <Payment> instance.
    """
    class PaymentStatus(models.TextChoices):
        """Payment status."""
        PENDING = 'PEND', 'Pending'
        SUCCESSFUL = 'SUCC', 'Successful'
        FAILED = 'FAIL', 'Failed'


    payment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments'
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='payment'
    )
    tx_ref = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=4, choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    chapa_transaction_id = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        """
        String representation of a <Payment> instance.
        """
        return f"Payment: {self.tx_ref} - {self.status}"
