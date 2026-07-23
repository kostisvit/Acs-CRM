from django.db import models
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Organization(TimeStampedModel):
    org_name = models.CharField(max_length=255, verbose_name="Πελάτης", blank=False)
    org_address = models.CharField(
        max_length=255, verbose_name="Διεύθυνση", blank=True, default="-"
    )
    org_city = models.CharField(
        max_length=255, verbose_name="Πόλη", blank=True, default="-"
    )
    org_phone = models.CharField(max_length=100, verbose_name="Τηλέφωνο", blank=False)
    org_remote = models.CharField(max_length=60, verbose_name="Remote", blank=True)
    org_email = models.EmailField(blank=True)
    org_site = models.URLField(max_length=250, blank=True, null=True)
    org_info = models.TextField(max_length=1000, verbose_name="Πληροφορίες", blank=True)
    is_visible = models.BooleanField(default=True, verbose_name="Κατάσταση")

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Οργανισμός"
        verbose_name_plural = "Οργανισμός"
        ordering = ["org_name"]

    def __str__(self):
        return self.org_name

    def soft_delete(self):
        self.is_visible = False
        self.save()

    def restore(self):
        self.is_visible = True
        self.save()

    @property
    def initials(self):
        words = self.org_name.split()

        if not words:
            return ""

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()


class Employee(TimeStampedModel):
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE, verbose_name="Οργανισμός", null=True)
    firstname = models.CharField(max_length=150, verbose_name="Όνομα", null=True)
    lastname = models.CharField(max_length=150, verbose_name="Επώνυμο", null=True)
    phone = models.CharField(max_length=100, verbose_name="Τηλέφωνο", blank=False)
    cellphone = models.CharField(max_length=30, verbose_name="Κινητό", blank=True)
    email = models.EmailField(blank=True, null=True)
    secondary_email = models.EmailField(blank=True, null=True)
    info = models.TextField(max_length=1000, verbose_name="Πληροφορίες", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Κατάσταση")
    org_department = models.ForeignKey(
        "parameters.OrgDepartment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τμήμα Οργανισμού",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Υπάλληλοι Οργανισμού"
        verbose_name_plural = "Υπάλληλοι Οργανισμού"

    def __str__(self):
        return (self.lastname or "") + " " + (self.firstname or "")

    def soft_delete(self):
        self.is_visible = False
        self.save()

    def restore(self):
        self.is_visible = True
        self.save()