# accounts/models.py

import datetime
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from .model_choices import *
from django.db.models import Q

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




class Adeia(models.Model):
    acs_employee = models.ForeignKey('User', max_length=100, verbose_name='Υπάλληλος', on_delete=models.CASCADE)
    adeiatype = models.CharField(max_length=1,choices=AdeiaChoices.choices,default=AdeiaChoices.KANONIKI, verbose_name='Τύπος Άδειας')
    startdate = models.DateField(default=datetime.date.today, verbose_name='Από')
    enddate = models.DateField(default=datetime.date.today, verbose_name='Έως')
    createddate = models.DateField(default=datetime.date.today, verbose_name='Ημ. Δημουργίας')
    days = models.IntegerField(verbose_name='Ημέρες', null=False, blank=False, default='0')

    class Meta:
        indexes = [models.Index(fields=['createddate', 'acs_employee'])]
        verbose_name = 'ACS Άδειες'
        verbose_name_plural = 'ACS Άδειες'

    def total(self):  # Προσθέτει τις μέρες άδειας του τρέχοντος έτους
        today = datetime.date.today()
        return self.__class__.objects.all().filter(createddate__year=today.year, acs_employee=self.acs_employee).exclude(Q(adeiatype='2') | Q(adeiatype='4')).aggregate(
            sum_all=Sum('days')).get('sum_all') or 0

    def anarotiki_total(self):
        today = datetime.date.today()
        return self.__class__.objects.all().filter(createddate__year=today.year, acs_employee=self.acs_employee, adeiatype='2').aggregate(
            sum_all=Sum('days')).get('sum_all')

    def goniki_total(self):
        today = datetime.date.today()
        return self.__class__.objects.all().filter(createddate__year=today.year, acs_employee=self.acs_employee, adeiatype='4').aggregate(
            sum_all=Sum('days')).get('sum_all')

    def kanoniki_total(self):
        today = datetime.date.today()
        return self.__class__.objects.all().filter(createddate__year=today.year, acs_employee=self.acs_employee, adeiatype='1').aggregate(
            sum_all=Sum('days')).get('sum_all')

    def get_absolute_url(self):
        return reverse('adeia_update', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('delete_adeia', args=[str(self.id)])