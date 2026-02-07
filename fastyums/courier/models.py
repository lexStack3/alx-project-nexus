import uuid
from django.db import models

from core.models import BaseModel
from orders.models import Order


class Delivery(BaseModel):
    """
    A model representation of a <Delivery> instance.
    """
    delivery_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='delivery'
    )
    
    def __str__(self):
        """
        String representation for a <Delivery> instance.
        """
        return f"Delivering of order: {self.order}"
