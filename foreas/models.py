from django.db import models
from django.urls import reverse


class Dhmos(models.Model):
    name = models.CharField(max_length=100, verbose_name='Πελάτης', blank=False)
    address = models.CharField(max_length=100, verbose_name='Διεύθυνση', blank=True, default='-')
    city = models.CharField(max_length=100, verbose_name='Πόλη', blank=True, default='-')
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