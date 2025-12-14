from django.db import transaction
from .models import Quote
from core.services.money import compute_line, quantize_money


@transaction.atomic
def recompute_quote_totals(quote: Quote) -> Quote:
    subtotal = tax_total = total = 0

    for line in quote.lines.select_for_update().all():
        ls, lt, ltot = compute_line(line.qty, line.unit_price, line.tax_rate)
        line.line_subtotal = ls
        line.line_tax = lt
        line.line_total = ltot
        line.save(update_fields=["line_subtotal", "line_tax", "line_total"])

        subtotal += ls
        tax_total += lt
        total += ltot

    quote.subtotal = quantize_money(subtotal)
    quote.tax_total = quantize_money(tax_total)
    quote.total = quantize_money(total)
    quote.save(update_fields=["subtotal", "tax_total", "total"])

    return quote
