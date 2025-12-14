from decimal import Decimal
from django.db import models
from core.models import TimeStampedModel


class Service(TimeStampedModel):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, default="forfait")  # ex: m², jour, forfait
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("20.00"),
        help_text="Tax rate in percent (e.g. 20.00 for 20%)",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name
