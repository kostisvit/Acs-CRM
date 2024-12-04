from django.db import models
from django.urls import reverse
from .model_choices import *
import datetime
from django.db.models import Sum

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


class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name='Πελάτης', blank=False,default='ACS')
    address = models.CharField(max_length=100, verbose_name='Διεύθυνση', blank=True,null=True )
    city = models.CharField(max_length=100, verbose_name='Πόλη', blank=True,null=True)
    phone = models.CharField(max_length=100, verbose_name='Τηλέφωνο', blank=False,null=True)
    fax = models.CharField(max_length=50, verbose_name='Fax', blank=True,null=True)
    teamviewer = models.CharField(max_length=60, verbose_name='TeamViewer', blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    website = models.URLField(max_length=250, blank=True, null=True)
    info = models.TextField(max_length=1000, verbose_name='Πληροφορίες', blank=True,null=True)
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
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, verbose_name='Πελάτης', null=True)
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

    # Custom managers
    objects = VisibilityManager()  # Filters only active objects

    def delete(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=false."""
        self.is_visible = False
        self.save()

    def restore(self, *args, **kwargs):
        """Soft delete the object by marking it as visible=true."""
        self.is_visible = True
        self.save()


class Ergasies(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, verbose_name='Πελάτης', default='-')
    importdate = models.DateField(default=datetime.date.today, verbose_name='Ημ. Κατ.', db_index=True)
    app = models.CharField(max_length=100, choices=app_choice,verbose_name='Εφαρμογή', blank=True)
    jobtype = models.CharField(max_length=100, choices=JobChoice.choices,verbose_name='Τύπος Εργασίας', default='TeamViewer')
    info = models.TextField(max_length=1000, verbose_name='Περιγραφή')
    text = models.TextField(max_length=1000, verbose_name='Σημειώσεις', blank=True)
    employee= models.ForeignKey('accounts.User', max_length=100, verbose_name='Υπάλληλος',on_delete=models.CASCADE, default='-')  # delete kai
    time = models.FloatField(verbose_name='Διάρκεια')
    name = models.CharField(max_length=100, verbose_name='Υπάλληλος Επικοιν.',null=True, help_text='Επώνυμο-Όνομα', blank=True)
    ticketid = models.CharField(max_length=50, verbose_name='Αίτημα OTS', blank=True)
    
    class Meta:
        indexes = [models.Index(fields=['importdate', 'employee'])]
        verbose_name = 'ACS Εργασίες Φορέα'
        verbose_name_plural = 'ACS Εργασίες Φορέα'
        ordering = ['importdate']
    
    def __str__(self):
        return str(self.id)
    
    def total_work_time(self):  # Ώρες εργασίας ανα χρήστη
        today = datetime.date.today()
        return Ergasies.objects.all().filter(importdate__year=today.year, employee=self.employee).aggregate(time_all=Sum('time')).get('time_all')

    def get_symbasi(self):
        return ",".join([str(p) for p in self.symbasi.all()])

    def get_absolute_url(self):
        return reverse('ergasia_update', args=[str(self.id)])
    
    def get_absolute_url_copy_paste(self):
        return reverse('ergasia_copy_paste', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('delete_ergasia', args=[str(self.id)])

    def get_admin_url_history(self):
        return reverse('admin:%s_%s_history' % (self._meta.app_label, self._meta.model_name),args=[self.id])
