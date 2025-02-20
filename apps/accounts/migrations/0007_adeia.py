# Generated by Django 5.1.3 on 2024-12-03 11:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adeia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adeiatype', models.CharField(blank=True, choices=[('1', 'Κανονική'), ('2', 'Αναρρωτική'), ('3', 'Εορταστική'), ('4', 'Γονική')], default='-', max_length=50, verbose_name='Τύπος Άδειας')),
                ('startdate', models.DateField(default=datetime.date.today, verbose_name='Από')),
                ('enddate', models.DateField(default=datetime.date.today, verbose_name='Έως')),
                ('createddate', models.DateField(default=datetime.date.today, verbose_name='Ημ. Δημουργίας')),
                ('days', models.IntegerField(default='0', verbose_name='Ημέρες')),
                ('acs_employee', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Υπάλληλος')),
            ],
            options={
                'verbose_name': 'ACS Άδειες',
                'verbose_name_plural': 'ACS Άδειες',
                'indexes': [models.Index(fields=['createddate', 'acs_employee'], name='accounts_ad_created_5c15cb_idx')],
            },
        ),
    ]
