import datetime
import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.parameters.models import OfficialHoliday


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(unique=True)

    # Permissions/admin fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Optional profile fields
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    allowed_leave_days = models.PositiveIntegerField(default=25)

    must_change_password = models.BooleanField(default=False)

    source_id = models.IntegerField(null=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email


class Adeia(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    acs_employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Υπάλληλος", on_delete=models.CASCADE)
    acs_adeiatype = models.ForeignKey(
        "parameters.AcsAdeia",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τύπος Άδειας",
    )
    startdate = models.DateField(
        default=datetime.date.today, verbose_name="Από")
    enddate = models.DateField(default=datetime.date.today, verbose_name="Έως")

    source_id = models.IntegerField(null=True, blank=True, unique=True)

    class Meta:
        indexes = (models.Index(fields=["acs_employee", "startdate"]),)
        verbose_name = "ACS Άδειες"
        verbose_name_plural = "ACS Άδειες"

    def working_days(self):
        days = 0
        current = self.startdate

        holidays = OfficialHoliday.objects.filter(
            date__range=(self.startdate, self.enddate)
        ).values_list("date", flat=True)

        holidays = set(holidays)

        while current <= self.enddate:
            if (
                current.weekday() < 5
                and current not in holidays
            ):
                days += 1

            current += datetime.timedelta(days=1)

        return days

    def clean(self):
        super().clean()

        overlap = Adeia.objects.filter(
            acs_employee=self.acs_employee,
            startdate__lte=self.enddate,
            enddate__gte=self.startdate,
        ).exclude(pk=self.pk)

        if overlap.exists():
            raise ValidationError(
                "Υπάρχει ήδη άδεια για αυτό το διάστημα."
            )
