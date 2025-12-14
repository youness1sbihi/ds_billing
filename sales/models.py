from decimal import Decimal
from django.db import models
from core.models import TimeStampedModel, CancelableModel
from customers.models import Customer
from catalog.models import Service


class QuoteStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    ACCEPTED = "accepted", "Accepted"
    CANCELLED = "cancelled", "Cancelled"


class Quote(TimeStampedModel, CancelableModel):
    number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="quotes")

    issue_date = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=15, choices=QuoteStatus.choices, default=QuoteStatus.DRAFT)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    tax_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-issue_date", "-id"]
        indexes = [
            models.Index(fields=["number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["issue_date"]),
        ]

    def __str__(self) -> str:
        return self.number


class QuoteLine(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="lines")

    # can be null when it's a free-text line
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.CharField(max_length=255, blank=True)

    qty = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("1.00"))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("20.00"))

    line_subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    line_tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
    # Auto-fill from selected service (only if missing)
        if self.service:
            if not self.description:
                self.description = self.service.name
            if not self.unit_price or self.unit_price == Decimal("0.00"):
                self.unit_price = self.service.unit_price
            if not self.tax_rate or self.tax_rate == Decimal("0.00"):
                self.tax_rate = self.service.tax_rate

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.quote.number} - line {self.id}"
