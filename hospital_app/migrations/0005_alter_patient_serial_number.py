# Generated by Django 5.1.4 on 2025-01-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0004_patient_serial_number_alter_labrequest_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='serial_number',
            field=models.CharField(max_length=255),
        ),
    ]
