from django.db import transaction
from invoicing.models import Invoice, InvoiceLine, InvoiceStatus
from core.services.numbering import build_number
from invoicing.services import recompute_invoice_totals
from .models import Quote, QuoteStatus


@transaction.atomic
def convert_quote_to_invoice(quote: Quote) -> Invoice:
    if quote.is_cancelled or quote.status == QuoteStatus.CANCELLED:
        raise ValueError("Cannot convert a cancelled quote.")

    if hasattr(quote, "invoice") and quote.invoice_id:
        return quote.invoice

    invoice = Invoice.objects.create(
        number=build_number("FAC", quote.issue_date),
        customer=quote.customer,
        source_quote=quote,
        issue_date=quote.issue_date,
        status=InvoiceStatus.DRAFT,
        notes=quote.notes,
    )

    lines = []
    for ql in quote.lines.all():
        lines.append(
            InvoiceLine(
                invoice=invoice,
                service=ql.service,
                description=ql.description,
                qty=ql.qty,
                unit_price=ql.unit_price,
                tax_rate=ql.tax_rate,
            )
        )
    InvoiceLine.objects.bulk_create(lines)

    recompute_invoice_totals(invoice)
    return invoice
