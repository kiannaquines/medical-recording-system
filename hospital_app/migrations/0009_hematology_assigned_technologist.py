# Generated by Django 5.1.4 on 2024-12-24 12:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0008_remove_hematology_others_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='hematology',
            name='assigned_technologist',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Medical Technologist'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_technologist', to=settings.AUTH_USER_MODEL),
        ),
    ]
