import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel
from encrypted_model_fields.fields import EncryptedCharField


class Customer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=150,  blank=True)
    company_type = models.CharField(max_length=150,  blank=True)
    company_address = models.CharField(max_length=150,  blank=True)
    company_email = models.EmailField(blank=True)
    company_afm = EncryptedCharField(max_length=150,  blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        verbose_name = "Πελάτες Ταμειακών Μηχανών"
        verbose_name_plural = "Πελάτες Ταμειακών Μηχανών"
        ordering = ["last_name"]
        db_table = "acs_tameiakes_customer"

    def __str__(self):
        return (self.lastname or "") + " " + (self.firstname or "")
