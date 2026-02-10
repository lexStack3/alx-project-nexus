import uuid
import pycountry

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation
)

from core.models import BaseModel


STATES = tuple((state.code, state.name) for state in
               pycountry.subdivisions.get(country_code='NG'))


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
        primary_key=True, default=uuid.uuid4, editable=False
    )
    role = models.CharField(
        max_length=3, choices=Roles.choices, default=Roles.CUSTOMER
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, unique=True
    )
    email = models.CharField(
        max_length=128, blank=False, unique=True
    )
    addresses = GenericRelation("Address")

    class Meta:
        indexes = [
            models.Index(
                fields=['email'],
                name='email_idx'
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'phone'],
                name='%(app_label)s_%(class)s_unique_email_phone'
            )
        ]

    def __str__(self):
        """A string representation of a <User> instance."""
        return self.username

    @property
    def full_name(self):
        """Returns the full name of a <User> instance."""
        if len(self.first_name) <= 0 or len(self.last_name) <= 0:
            full_name = self.username
        else:
            full_name = f"{self.first_name} {self.last_name}"
        return f"{full_name}"


class Address(BaseModel):
    """
    A model representation of a <Address> instance.
    """
    address_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        max_length=128, blank=True, default=''
    )
    street = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=128, blank=False)
    state = models.CharField(
        max_length=50, choices=STATES, default='NG-CR', blank=False
    )
    country = models.CharField(
        max_length=10, default='Nigeria', editable=False
    )

    is_default = models.BooleanField(default=False)

    # GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                condition=models.Q(is_default=True),
                name='unique_default_address_per_owner'
            )
        ]

    def __str__(self):
        return "{}, {} - {}, {}".format(
                    self.street,
                    self.city,
                    self.state,
                    self.country
                )

    @property
    def full_address(self):
        return "{}, {} - {}, {}".format(
                    self.street,
                    self.city,
                    self.state,
                    self.country
                )

    @property
    def to_dict(self):
        """
        Returns a dictionary of all the key-value pairs in the <Address> instance.
        """
        return {
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'country': self.country
        }
