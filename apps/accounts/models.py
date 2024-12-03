# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

class Company(TimeStampedModel):
    company_owner_name = models.CharField(max_length=255)
    company_title = models.CharField(max_length=255)
    company_title_alias = models.CharField(max_length=255, unique=True)
    company_address = models.CharField(max_length=255)
    company_city = models.CharField(max_length=100)
    company_postal_code = models.CharField(max_length=20)
    company_country = models.CharField(max_length=100)
    company_phone_number_1 = models.CharField(max_length=255)
    company_phone_number_2 = models.CharField(max_length=255)
    company_email = models.EmailField(max_length=254)
    company_is_active = models.BooleanField(default=True)
    
    
    
    class Meta:
        ordering = ['company_title']
        verbose_name = _('Εταιρεία')
        verbose_name_plural = _('Εταιρεία')
    
    def __str__(self):
        return f"{self.company_title}"



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    company = models.ManyToManyField(Company, related_name="users")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True,null=True, blank=True)
    first_login = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


