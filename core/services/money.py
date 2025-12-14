from decimal import Decimal, ROUND_HALF_UP


Q = Decimal("0.01")


def quantize_money(value: Decimal) -> Decimal:
    return (value or Decimal("0.00")).quantize(Q, rounding=ROUND_HALF_UP)


def compute_line(qty: Decimal, unit_price: Decimal, tax_rate: Decimal) -> tuple[Decimal, Decimal, Decimal]:
    qty = qty or Decimal("0.00")
    unit_price = unit_price or Decimal("0.00")
    tax_rate = tax_rate or Decimal("0.00")

    subtotal = qty * unit_price
    tax = subtotal * (tax_rate / Decimal("100.00"))
    total = subtotal + tax

    return quantize_money(subtotal), quantize_money(tax), quantize_money(total)
