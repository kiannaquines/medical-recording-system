# Generated by Django 5.1.4 on 2024-12-24 12:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0009_hematology_assigned_technologist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='hematology',
            name='assigned_pathologist',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Pathologist'}, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_pathologist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hematology',
            name='assigned_technologist',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Medical Technologist'}, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_technologist', to=settings.AUTH_USER_MODEL),
        ),
    ]
