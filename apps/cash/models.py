import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
from encrypted_model_fields.fields import EncryptedCharField


class Customer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField("Επωνυμία", max_length=200)
    vat_number = EncryptedCharField(
        "ΑΦΜ", max_length=9, unique=True
    )
    phone = models.CharField(
        "Τηλέφωνο", max_length=30, blank=True
    )
    email = models.EmailField(blank=True)
    address = models.CharField(
        "Διεύθυνση", max_length=255, blank=True
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    source_id = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = "Πελάτης"
        verbose_name_plural = "Πελάτες"
        ordering = ["-created"]
        db_table = "cash_customer"

    def __str__(self):
        return f"{self.name} ({self.vat_number})"
