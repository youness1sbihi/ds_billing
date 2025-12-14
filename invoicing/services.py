from django.db import transaction
from .models import Invoice
from core.services.money import compute_line, quantize_money


@transaction.atomic
def recompute_invoice_totals(invoice: Invoice) -> Invoice:
    subtotal = tax_total = total = 0

    for line in invoice.lines.select_for_update().all():
        ls, lt, ltot = compute_line(line.qty, line.unit_price, line.tax_rate)
        line.line_subtotal = ls
        line.line_tax = lt
        line.line_total = ltot
        line.save(update_fields=["line_subtotal", "line_tax", "line_total"])

        subtotal += ls
        tax_total += lt
        total += ltot

    invoice.subtotal = quantize_money(subtotal)
    invoice.tax_total = quantize_money(tax_total)
    invoice.total = quantize_money(total)
    invoice.save(update_fields=["subtotal", "tax_total", "total"])

    return invoice
