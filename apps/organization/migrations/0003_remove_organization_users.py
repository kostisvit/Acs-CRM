# Generated by Django 5.1.3 on 2024-11-22 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='users',
        ),
    ]
