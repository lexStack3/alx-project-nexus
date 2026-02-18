import uuid
from django.db import models

from core.models import BaseModel
from vendors.models import Vendor


class Category(BaseModel):
    """
    A model representation of a <Category> instance.
    """
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        String representation of a <Category> instance.
        """
        return self.name

    class Meta:
        indexes = [
            models.Index(
                fields=['name'],
                name='category_name_idx'
            )
        ]


class Product(BaseModel):
    """
    A model representation of a <Product> instance.
    """
    product_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=128, blank=False)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00
    )
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation of a <Product> instance.
        """
        return f"Name: {self.name} - Qty: {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vendor', 'name'],
                name='unique_product_per_vendor'
            )
        ]
        indexes = [
            models.Index(
                fields=['name'],
                name='product_name_idx'
            )
        ]
        ordering = ['name']

    @property
    def owner(self):
        return self.vendor.owner
