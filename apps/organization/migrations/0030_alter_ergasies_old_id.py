# Generated by Django 5.1.4 on 2025-01-24 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0029_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ergasies',
            name='old_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='old_id'),
        ),
    ]
