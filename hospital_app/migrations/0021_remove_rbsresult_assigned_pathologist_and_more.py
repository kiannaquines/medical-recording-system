# Generated by Django 5.1.4 on 2024-12-29 05:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0020_remove_rbs_assigned_pathologist_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rbsresult',
            name='assigned_pathologist',
        ),
        migrations.RemoveField(
            model_name='rbsresult',
            name='assigned_technologist',
        ),
        migrations.AddField(
            model_name='rbs',
            name='assigned_pathologist',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Pathologist'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rbs_assigned_pathologist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rbs',
            name='assigned_technologist',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Medical Technologist'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rbs_assigned_technologist', to=settings.AUTH_USER_MODEL),
        ),
    ]
