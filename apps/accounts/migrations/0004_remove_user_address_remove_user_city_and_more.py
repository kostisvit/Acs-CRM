# Generated by Django 5.1.3 on 2024-12-03 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_company_owner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='user',
            name='postal_code',
        ),
    ]
