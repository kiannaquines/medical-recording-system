# Generated by Django 5.1.4 on 2024-12-27 16:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0019_alter_crossmatching_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rbs',
            name='assigned_pathologist',
        ),
        migrations.RemoveField(
            model_name='rbs',
            name='assigned_technologist',
        ),
        migrations.RemoveField(
            model_name='rbs',
            name='date',
        ),
        migrations.RemoveField(
            model_name='rbs',
            name='result',
        ),
        migrations.RemoveField(
            model_name='rbs',
            name='time',
        ),
        migrations.CreateModel(
            name='RBSResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('assigned_pathologist', models.ForeignKey(limit_choices_to={'groups__name': 'Pathologist'}, on_delete=django.db.models.deletion.CASCADE, related_name='rbs_assigned_pathologist', to=settings.AUTH_USER_MODEL)),
                ('assigned_technologist', models.ForeignKey(limit_choices_to={'groups__name': 'Medical Technologist'}, on_delete=django.db.models.deletion.CASCADE, related_name='rbs_assigned_technologist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rbs',
            name='rbs_result',
            field=models.ManyToManyField(help_text='Related RBS results.', related_name='rbs_results', to='hospital_app.rbsresult'),
        ),
    ]
