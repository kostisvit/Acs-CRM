import re
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
    source_id = models.UUIDField(
            default=uuid.uuid4,
            editable=False)

    class Meta:
        verbose_name = "Πελάτης"
        verbose_name_plural = "Πελάτες"
        ordering = ["-created"]
        db_table = "cash_customer"

    def __str__(self):
        return f"{self.name} ({self.vat_number})"


    @property
    def initials(self):
        # Remove symbols and keep only letters/spaces
        clean_name = re.sub(r'[^\w\s]', '', self.name)

        words = clean_name.split()

        if not words:
            return ""

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()



class CashRegisterModel(TimeStampedModel):
    manufacturer = models.CharField(
        "Κατασκευαστής", max_length=100
    )
    name = models.CharField(
        "Μοντέλο", max_length=100
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Μοντέλο ταμειακής"
        verbose_name_plural = "Μοντέλα ταμειακών"
        constraints = [
            models.UniqueConstraint(
                fields=["manufacturer", "name"],
                name="unique_cash_register_model",
            )
        ]

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


class SoftwareVersion(TimeStampedModel):
    version_number = models.CharField(
        "Αριθμός έκδοσης", max_length=50
    )
    release_date = models.DateField(
        "Ημερομηνία κυκλοφορίας", null=True, blank=True
    )
    compatible_models = models.ManyToManyField(
        CashRegisterModel,
        blank=True,
        related_name="software_versions",
        verbose_name="Συμβατά μοντέλα",
    )
    release_notes = models.TextField(
        "Σημειώσεις έκδοσης", blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Έκδοση λογισμικού"
        verbose_name_plural = "Εκδόσεις λογισμικού"
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["version_number"],
                name="unique_software_version_number",
            )
        ]

    def __str__(self):
        return self.version_number
