from django.db import models

class BaseModel(models.Model):
    """
    An abstract base model to be inherited by other models for common fields:
    -   created_at
    -   updated_at
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']