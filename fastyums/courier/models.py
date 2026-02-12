import uuid
from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from orders.models import Order


User = get_user_model()


class Delivery(BaseModel):
    """
    A model representation of a <Delivery> instance.
    Handles the logistics lifecycle of an order.
    """
    class DeliveryStatus(models.TextChoices):
        PENDING = 'PEND', 'Pending'
        ASSIGNED = 'ASGN', 'Assigned'
        IN_TRANSIT = 'TRANS', 'In Transit'
        DELIVERED = 'DELD', 'Delivered'
        FAILED = 'FAIL', 'Failed'

    delivery_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    courier = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='deliveries'
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='delivery'
    )
    status = models.CharField(
        max_length=5,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING
    )
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        String representation for a <Delivery> instance.
        """
        return f"Delivering of order: {self.order}"

    @property
    def owner(self):
        return self.order.iser
