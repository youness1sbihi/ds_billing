from django.db import models
from core.models import TimeStampedModel


class Customer(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, blank=True)

    # Morocco business IDs (optional)
    ice = models.CharField(max_length=30, blank=True)
    if_tax = models.CharField("IF", max_length=30, blank=True)
    rc = models.CharField(max_length=30, blank=True)
    cnss = models.CharField(max_length=30, blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self) -> str:
        return self.name
