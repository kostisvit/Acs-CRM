# Generated by Django 5.1.3 on 2024-12-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_alter_ergasies_org_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Κατάσταση'),
        ),
    ]
