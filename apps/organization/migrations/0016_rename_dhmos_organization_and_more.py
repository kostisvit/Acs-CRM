# Generated by Django 5.1.3 on 2024-12-05 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0015_rename_organization_dhmos_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dhmos',
            new_name='Organization',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='dhmos',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='ergasies',
            old_name='dhmos',
            new_name='organization',
        ),
    ]
