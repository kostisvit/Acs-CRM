# Generated by Django 5.1.4 on 2024-12-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0022_alter_ergasies_org_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ergasies',
            name='jobtype',
            field=models.CharField(choices=[('TeamViewer', 'TeamViewer'), ('Επίσκεψη', 'Επίσκεψη'), ('Γραφείο', 'Γραφείο'), ('Webinar-Zoom', 'Webinar-Zoom')], default='TeamViewer', max_length=100, verbose_name='Τύπος Εργασίας'),
        ),
    ]
