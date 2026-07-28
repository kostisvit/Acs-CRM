from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.conf import settings
import datetime
from django.core.exceptions import ValidationError

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

    email = models.EmailField(unique=True)

    # Permissions/admin fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Optional profile fields
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    must_change_password = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email




class Adeia(TimeStampedModel):
    acs_employee = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="Υπάλληλος", on_delete=models.CASCADE)
    acs_adeiatype = models.ForeignKey(
        "parameters.AcsAdeia",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Τύπος Άδειας",
    )
    startdate = models.DateField(default=datetime.date.today, verbose_name="Από")
    enddate = models.DateField(default=datetime.date.today, verbose_name="Έως")

    class Meta:
        indexes = [models.Index(fields=["acs_employee"])]
        verbose_name = "ACS Άδειες"
        verbose_name_plural = "ACS Άδειες"

    @property
    def days(self):
        return (self.enddate - self.startdate).days + 1

    def clean(self):
        if self.enddate < self.startdate:
            raise ValidationError("End date cannot be before start date.")

        if self.days < 0:
            raise ValidationError("Days cannot be negative.")

    def get_absolute_url(self):
        return reverse("acs_adeia_update", args=[str(self.id)])  # type: ignore

    def get_absolute_url_delete(self):
        return reverse("acs_adeia_delete", args=[str(self.id)])  # type: ignore