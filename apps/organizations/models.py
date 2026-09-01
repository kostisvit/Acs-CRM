import datetime
import re
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Organization(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    org_name = models.CharField(
        max_length=255, verbose_name="Πελάτης", blank=False)
    org_address = models.CharField(
        max_length=255, verbose_name="Διεύθυνση", blank=True, default="-"
    )
    org_city = models.CharField(
        max_length=255, verbose_name="Πόλη", blank=True, default="-"
    )
    org_phone = models.CharField(
        max_length=100, verbose_name="Τηλέφωνο", blank=False)
    org_remote = models.CharField(
        max_length=60, verbose_name="Remote", blank=True)
    org_email = models.EmailField(blank=True)
    org_site = models.URLField(max_length=250, blank=True, null=True)
    org_info = models.TextField(
        max_length=1000, verbose_name="Πληροφορίες", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Κατάσταση")

    source_id = models.IntegerField(blank=True, null=True, unique=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Οργανισμός"
        verbose_name_plural = "Οργανισμός"
        ordering = ("org_name",)

    def __str__(self):
        return self.org_name

    def soft_delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()

    @property
    def initials(self):
        # Remove symbols and keep only letters/spaces
        clean_name = re.sub(r'[^\w\s]', '', self.org_name)

        words = clean_name.split()

        if not words:
            return ""

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()


class Employee(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE,
                                     related_name="employees", verbose_name="Οργανισμός", null=True)
    firstname = models.CharField(
        max_length=150, verbose_name="Όνομα", blank=True)
    lastname = models.CharField(
        max_length=150, verbose_name="Επώνυμο", blank=True)
    phone = models.CharField(
        max_length=100, verbose_name="Τηλέφωνο", blank=False)
    mobile = models.CharField(max_length=30, verbose_name="Κινητό", blank=True)
    email = models.EmailField(blank=True, null=True, db_index=True)
    secondary_email = models.EmailField(blank=True, null=True)
    info = models.TextField(
        max_length=1000, verbose_name="Πληροφορίες", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Κατάσταση")
    org_department = models.ForeignKey(
        "parameters.OrgDepartment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τμήμα Οργανισμού",
    )

    source_id = models.IntegerField(blank=True, null=True, unique=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Υπάλληλοι Οργανισμού"
        verbose_name_plural = "Υπάλληλοι Οργανισμού"
        ordering = ("lastname", "firstname")

    def __str__(self):
        return (self.lastname or "") + " " + (self.firstname or "")

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    @property
    def initials(self):
        full_name = f"{self.firstname or ''} {self.lastname or ''}".strip()

        if not full_name:
            return ""

        words = full_name.split()

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()

    def soft_delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()


class Task(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    organization = models.ForeignKey(
        "Organization", on_delete=models.PROTECT, verbose_name="Οργανισμός")
    importdate = models.DateField(
        default=timezone.localdate, verbose_name="Ημ. Κατ.", db_index=True)
    org_app = models.ForeignKey(
        "parameters.OtsSoftware",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Εφαρμογή OTS",
    )
    job_type_acs = models.ForeignKey(
        "parameters.JobType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τύπος Εργασίας ACS",
    )
    task_info = models.TextField(
        max_length=1000, verbose_name="Περιγραφή εργασίας")
    task_note = models.TextField(
        max_length=1000, verbose_name="Σημειώσεις", blank=True)
    acs_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Υπάλληλος",
        on_delete=models.PROTECT,
    )
    task_time = models.DecimalField(verbose_name="Διάρκεια εργασίας",
                                    max_digits=5, decimal_places=2, validators=[MinValueValidator(0)],)
    org_employee = models.ForeignKey(
        "Employee",
        on_delete=models.PROTECT,
        verbose_name="Υπάλληλος",
        null=True,
        blank=True,
    )
    ticketid = models.CharField(
        max_length=50, verbose_name="Αίτημα OTS", null=True, blank=True)

    source_id = models.IntegerField(blank=True, null=True, unique=True)

    history = HistoricalRecords()

    class Meta:
        indexes = (models.Index(
            fields=["organization", "importdate", "acs_employee"]),)
        verbose_name = "Εργασίες Οργανισμού"
        verbose_name_plural = "Εργασίες Οργανισμού"
        ordering = ("-importdate",)

    def __str__(self):
        return str(self.organization)

    def task_time_count(self):  # Ώρες εργασίας ανα χρήστη
        today = datetime.datetime.now(tz=datetime.UTC).date()
        return (
            Task.objects.all()
            .filter(importdate__year=today.year, acs_employee=self.acs_employee)
            .aggregate(task_time_sum=Sum("task_time"))
            .get("task_time_sum")
        )


class Training(TimeStampedModel):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, verbose_name="Οργανισμός", null=True, blank=True)
    training_date = models.DateField(
        default=timezone.localdate, verbose_name="Ημερομηνία Εκπαίδευσης")
    org_app = models.ForeignKey(
        "parameters.OtsSoftware",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Εφαρμογή OTS",
    )
    training_type = models.ForeignKey(
        "parameters.TrainingType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τύπος Εκπαίδευσης",
    )
    training_time = models.DecimalField(verbose_name="Διάρκεια εργασίας",
                                        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)],)
    acs_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Υπάλληλος",
        on_delete=models.PROTECT,
    )
    training_info = models.TextField(
        max_length=500, verbose_name="Περιγραφή", null=True, blank=True)
    training_note = models.TextField(
        max_length=500, verbose_name="Σημειώσεις", null=True, blank=True)

    class Meta:
        indexes = (models.Index(fields=["training_date", "acs_employee"]),)
        verbose_name = "ACS Εκπαιδεύσεις"
        verbose_name_plural = "ACS Εκπαιδεύσεις"
