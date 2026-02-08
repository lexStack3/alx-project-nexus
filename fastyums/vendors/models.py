import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

from core.models import BaseModel
from accounts.models import Address


User = get_user_model()


class Vendor(BaseModel):
    """
    A model representation of a <Vendor> instance.
    """
    vendor_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    addresses = GenericRelation(Address)

    def __str__(self):
        """
        String representation of a <Vendor> instance.
        """
        return self.name
