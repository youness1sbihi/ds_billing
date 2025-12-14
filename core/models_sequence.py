from django.db import models


class Sequence(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.key}={self.value}"
