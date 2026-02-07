from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel


User = get_user_model()


class Vendor(BaseModel):
    """
    A model representation of a <Vendor> instance.
    """
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation of a <Vendor> instance.
        """
        return self.name
