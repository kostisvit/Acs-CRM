import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel

class JobType(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    source_id = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = "Τύπος Εργασίας"
        verbose_name_plural = "Τύπος Εργασίας"

    def __str__(self):
        return self.name


class OtsSoftware(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="Όνομα Εφαρμογής")
    is_active = models.BooleanField(default=True, verbose_name="Ενεργή")

    source_id = models.IntegerField(null=True, unique=True)
    
    class Meta:
        verbose_name = "Λογισμικό Οργανισμού"
        verbose_name_plural = "Λογισμικό Οργανισμού"

    def __str__(self):
        return self.name


class OrgDepartment(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    source_id = models.IntegerField(null=True, unique=True)

    class Meta:
        verbose_name = "Διευθύνσεις Οργανισμού"
        verbose_name_plural = "Διευθύνσεις Οργανισμού"

    def __str__(self):
        return self.name


class TrainingType(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Εκπαίδευση"
        verbose_name_plural = "Εκπαίδευση"

    def __str__(self):
        return self.name


class TrainingPlace(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )    
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Χώρος Εκπαίδευσης"
        verbose_name_plural = "Χώρος Εκπαίδευσης"

    def __str__(self):
        return self.name


class AcsAdeia(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="Τύπος Άδειας")
    adeianame_id = models.CharField(
        unique=True, verbose_name="ID Τύπου Άδειας", blank=True, null=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Ενεργή")

    source_id = models.IntegerField(null=True, unique=True)
    
    class Meta:
        verbose_name = "ACS Τύπος Άδειας"
        verbose_name_plural = "ACS Τύποι Άδειας"

    def __str__(self):
        return self.name



class OfficialHoliday(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    date = models.DateField(unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.date} - {self.description}"