from datetime import date
from core.services.sequences import next_sequence


def build_number(prefix: str, on_date: date) -> str:
    year = on_date.year
    seq = next_sequence(f"{prefix}-{year}")
    return f"{prefix}-{year}-{seq:04d}"
