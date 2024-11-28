from django.db import models
from django.urls import reverse
from .model_choices import *

class VisibilityManager(models.Manager):
    """
    Custom manager to handle visibility filters.
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Override the default queryset to include all records.
        """
        return super().get_queryset()

    def visible(self) -> models.QuerySet:
        """
        Return only records where is_visible=True.
        """
        return self.get_queryset().filter(is_visible=True)

    def invisible(self) -> models.QuerySet:
        """
        Return only records where is_visible=False.
        """
        return self.get_queryset().filter(is_visible=False)


class Dhmos(models.Model):
    name = models.CharField(max_length=100, verbose_name='Πελάτης', blank=False)
    address = models.CharField(max_length=100, verbose_name='Διεύθυνση', blank=True, )
    city = models.CharField(max_length=100, verbose_name='Πόλη', blank=True,)
    phone = models.CharField(max_length=100, verbose_name='Τηλέφωνο', blank=False)
    fax = models.CharField(max_length=50, verbose_name='Fax', blank=True)
    teamviewer = models.CharField(max_length=60, verbose_name='TeamViewer', blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    info = models.TextField(max_length=1000, verbose_name='Πληροφορίες', blank=True)
    is_visible = models.BooleanField(default=False, verbose_name='Κατάσταση')

    class Meta:
        verbose_name = 'ACS Φορέας'
        verbose_name_plural = 'ACS Φορέας'
        ordering = ['name']

    # Custom managers
    objects = VisibilityManager()  # Filters only active objects

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=false."""
        self.is_visible = False
        self.save()

    def restore(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=true."""
        self.is_visible = True
        self.save()



class Employee(models.Model):
    dhmos = models.ForeignKey('Dhmos', on_delete=models.CASCADE, verbose_name='Πελάτης', null=True)
    firstname = models.CharField(max_length=150, verbose_name='Όνομα', null=True)
    lastname = models.CharField(max_length=150, verbose_name='Επώνυμο', null=True)
    tmhma = models.CharField(max_length=100, choices=tmhma_choice,verbose_name='Υπηρεσία', blank=True, null=True,)
    phone = models.CharField(max_length=100, verbose_name='Τηλέφωνο', blank=False)
    cellphone = models.CharField(max_length=30, verbose_name='Κινητό', blank=True)
    email = models.EmailField(blank=True, null=True)
    secondary_email = models.EmailField(blank=True, null=True)
    info = models.TextField(max_length=1000, verbose_name='Πληροφορίες', blank=True)
    is_visible = models.BooleanField(default=False, verbose_name='Κατάσταση')

    class Meta:
        verbose_name = 'ACS Στοιχεία Επικοινωνίας Υπαλλήλων'
        verbose_name_plural = 'ACS Στοιχεία Επικοινωνίας Υπαλλήλων'

    def __str__(self):
        return (self.lastname) + " " + (self.firstname)

    def delete(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=false."""
        self.is_visible = False
        self.save()

    def restore(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=true."""
        self.is_visible = True
        self.save()