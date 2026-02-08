import uuid
from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from categories.models import Product


User = get_user_model()


class Order(BaseModel):
    """
    A model representation of a <Order> instance.
    """
    class Status(models.TextChoices):
        """Order status choices."""
        PENDING = 'PEND', 'Pending'
        PAID = 'PAID', 'Paid'
        DELIVERED = 'DELD', 'Delivered'
        CANCELLED = 'CANC', 'Cancelled'


    order_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING
    )
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    address = models.JSONField()

    def __str__(self):
        """
        String representation of an <Order> instance.
        """
        return f"{self.order_id} - ₦{self.total_price}"


class OrderItem(BaseModel):
    """
    A model representation of an <OrderItem> instance.
    """
    item_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        """
        String representation of a <OrderItem> instance.
        """
        return f"{self.product.name} - {self.quantity}"
