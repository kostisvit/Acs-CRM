# Generated by Django 5.1.4 on 2024-12-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0016_rename_dhmos_organization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='old_id',
            field=models.IntegerField(null=True, verbose_name='old_id'),
        ),
    ]
