import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    An abstract base model to be inherited by other models for common fields:
    -   created_at
    -   updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        pass

    class Meta:
        abstract = True
        ordering = ['-created_at']


class User(AbstractUser, BaseModel):
    """A model representation of a <User> instance."""
    class Roles(models.TextChoices):
        # User roles
        CUSTOMER = 'CUS', 'Customer'
        VENDOR = 'VEN', 'Vendor'
        COURIER = 'COU', 'Courier'
        ADMIN = 'ADM', 'Admin'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        max_length=3,
        choices=Roles.choices,
        default=Roles.CUSTOMER
    )
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    email = models.CharField(max_length=128, blank=False, unique=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['email'],
                name='email_idx'
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'phone_number'],
                name='%(app_label)s_%(class)s_unique_email_phone_number'
            )
        ]
