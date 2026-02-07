import uuid
from django.db import models

from core.models import BaseModel
from vendor.models import Vendor


class Category(BaseModel):
    """
    A model representation of a <Category> instance.
    """
    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        String representation of a <Category> instance.
        """
        return self.name


class Product(BaseModel):
    """
    A model representation of a <Product> instance.
    """
    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=128, blank=False)
    price = models.DecimalField(
        max_digits=8
        decimal_places=2,
        default=0.00
    )
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation of a <Product> instance.
        """
        return f"Name: {self.name} - Qty: {self.quantity}"

