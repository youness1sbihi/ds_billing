from decimal import Decimal
from django.db import models
from core.models import TimeStampedModel, CancelableModel
from customers.models import Customer
from catalog.models import Service
from sales.models import Quote


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ISSUED = "issued", "Issued"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class Invoice(TimeStampedModel, CancelableModel):
    number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="invoices")

    # One invoice per quote (optional)
    source_quote = models.OneToOneField(
        Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoice"
    )

    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=15, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)

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


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    qty = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("1.00"))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("20.00"))

    line_subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    line_tax = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.invoice.number} - line {self.id}"
