from django.db import models
from django.urls import reverse
from .model_choices import *


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pelatis_update', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('delete_pelatis', args=[str(self.id)])
    
    def get_admin_url_history(self):
        return reverse('admin:%s_%s_history' % (self._meta.app_label, self._meta.model_name),args=[self.id])



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

    def get_absolute_url(self):
        return reverse('epafi_update', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('delete_epafi', args=[str(self.id)])