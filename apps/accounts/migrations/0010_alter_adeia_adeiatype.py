# Generated by Django 5.1.4 on 2024-12-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_training_remove_adeia_accounts_ad_created_5c15cb_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adeia',
            name='adeiatype',
            field=models.CharField(choices=[('1', 'Κανονική'), ('2', 'Αναρρωτική'), ('3', 'Εορταστική')], max_length=1, verbose_name='Τύπος Άδειας'),
        ),
    ]
