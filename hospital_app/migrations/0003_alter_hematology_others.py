# Generated by Django 5.1.4 on 2024-12-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0002_alter_crossmatching_medical_technologist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hematology',
            name='others',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
