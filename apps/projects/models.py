import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from apps.organizations.models import Organization


class Project(TimeStampedModel):
    """
    Έργο που ανήκει σε έναν Οργανισμό.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name="Οργανισμός",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Τίτλος έργου",
    )

    description = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Περιγραφή",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ημερομηνία έναρξης",
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ημερομηνία λήξης",
    )

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="responsible_projects",
        verbose_name="Υπεύθυνος",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Ενεργό",
    )

    info = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Πληροφορίες",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Έργο"
        verbose_name_plural = "Έργα"
        ordering = ("-created",)
        indexes = (
            models.Index(
                fields=["organization", "is_active"],
            ),
            models.Index(
                fields=["end_date"],
            ),
            models.Index(
                fields=["responsible", "is_active"],
            ),
        )

    def __str__(self):
        return self.title

    @property
    def documents_count(self):
        return self.documents.count()

    @property
    def completed_documents_count(self):
        return self.documents.filter(submitted=True).count()

    @property
    def pending_documents_count(self):
        return self.documents.filter(submitted=False).count()

    @property
    def overdue_documents_count(self):
        today = timezone.localdate()

        return self.documents.filter(
            submitted=False,
            due_date__lt=today,
        ).count()

    @property
    def is_overdue(self):
        """
        Επιστρέφει True αν το έργο έχει περάσει την ημερομηνία λήξης.
        """
        if not self.end_date:
            return False

        return self.end_date < timezone.localdate() and self.is_active

    @property
    def days_until_end(self):
        """
        Πόσες ημέρες απομένουν μέχρι τη λήξη του έργου.
        """
        if not self.end_date:
            return None

        return (self.end_date - timezone.localdate()).days


class ProjectDocument(TimeStampedModel):
    """
    Έντυπο / παραδοτέο ενός έργου.

    Κάθε Project μπορεί να έχει πολλά ProjectDocument.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Έργο",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Έντυπο",
    )

    description = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Περιγραφή",
    )

    due_date = models.DateField(
        db_index=True,
        verbose_name="Ημερομηνία παράδοσης",
    )

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="responsible_project_documents",
        verbose_name="Υπεύθυνος",
    )

    file = models.FileField(
        upload_to="projects/documents/",
        null=True,
        blank=True,
        verbose_name="Αρχείο",
    )

    submitted = models.BooleanField(
        default=False,
        verbose_name="Υποβλήθηκε",
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ημερομηνία υποβολής",
    )

    notes = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name="Σημειώσεις",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Έντυπο έργου"
        verbose_name_plural = "Έντυπα έργου"
        ordering = ("due_date",)
        indexes = (
            models.Index(
                fields=["project", "due_date"],
            ),
            models.Index(
                fields=["submitted", "due_date"],
            ),
            models.Index(
                fields=["responsible", "submitted", "due_date"],
            ),
        )

    def __str__(self):
        return f"{self.project} - {self.title}"

    @property
    def is_overdue(self):
        """
        True αν το έντυπο δεν έχει υποβληθεί
        και έχει περάσει η ημερομηνία παράδοσης.
        """
        return (
            not self.submitted
            and self.due_date < timezone.localdate()
        )

    @property
    def days_until_due(self):
        """
        Θετικός αριθμός = ημέρες μέχρι την προθεσμία.
        0 = λήγει σήμερα.
        Αρνητικός = εκπρόθεσμο.
        """
        return (self.due_date - timezone.localdate()).days

    @property
    def status(self):
        """
        Επιστρέφει απλό status για χρήση σε templates / dashboard.
        """

        if self.submitted:
            return "submitted"

        if self.is_overdue:
            return "overdue"

        days = self.days_until_due

        if days == 0:
            return "due_today"

        if days <= 3:
            return "urgent"

        if days <= 7:
            return "warning"

        return "pending"

    def mark_as_submitted(self):
        """
        Μαρκάρει το έντυπο ως υποβληθέν.
        """

        self.submitted = True
        self.submitted_at = timezone.now()
        self.save(
            update_fields=[
                "submitted",
                "submitted_at",
                "modified",
            ]
        )

    def mark_as_pending(self):
        """
        Επαναφέρει το έντυπο σε εκκρεμότητα.
        """

        self.submitted = False
        self.submitted_at = None
        self.save(
            update_fields=[
                "submitted",
                "submitted_at",
                "updated_at",
            ]
        )


class ProjectReminder(TimeStampedModel):
    """
    Υπενθύμιση για συγκεκριμένο έντυπο.

    Παράδειγμα:
        days_before = 7
        days_before = 3
        days_before = 1

    Όταν το σύστημα φτάσει στην αντίστοιχη ημερομηνία,
    μπορεί να στείλει notification/email.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    document = models.ForeignKey(
        ProjectDocument,
        on_delete=models.CASCADE,
        related_name="reminders",
        verbose_name="Έντυπο",
    )

    days_before = models.PositiveIntegerField(
        default=3,
        validators=[
            MinValueValidator(0),
        ],
        verbose_name="Ημέρες πριν",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Ενεργή",
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ημερομηνία αποστολής",
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Υπενθύμιση εντύπου"
        verbose_name_plural = "Υπενθυμίσεις εντύπων"
        ordering = ("days_before",)

        constraints = [
            models.UniqueConstraint(
                fields=["document", "days_before"],
                name="unique_document_reminder_days",
            ),
        ]

        indexes = (
            models.Index(
                fields=["is_active", "sent_at"],
            ),
        )

    def __str__(self):
        return (
            f"{self.document} - "
            f"{self.days_before} ημέρες πριν"
        )

    @property
    def reminder_date(self):
        """
        Η ημερομηνία κατά την οποία πρέπει να ενεργοποιηθεί
        η υπενθύμιση.
        """

        return self.document.due_date - timezone.timedelta(
            days=self.days_before
        )

    @property
    def should_send(self):
        """
        Ελέγχει αν πρέπει να σταλεί η υπενθύμιση τώρα.
        """

        if not self.is_active:
            return False

        if self.sent_at is not None:
            return False

        if self.document.submitted:
            return False

        return timezone.localdate() >= self.reminder_date

    def mark_as_sent(self):
        """
        Μαρκάρει την υπενθύμιση ως απεσταλμένη.
        """

        self.sent_at = timezone.now()
        self.save(
            update_fields=[
                "sent_at",
                "updated_at",
            ]
        )
