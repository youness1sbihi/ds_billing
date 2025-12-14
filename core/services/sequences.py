from django.db import transaction
from core.models_sequence import Sequence


@transaction.atomic
def next_sequence(key: str) -> int:
    seq, _ = Sequence.objects.select_for_update().get_or_create(key=key, defaults={"value": 0})
    seq.value += 1
    seq.save(update_fields=["value"])
    return seq.value
