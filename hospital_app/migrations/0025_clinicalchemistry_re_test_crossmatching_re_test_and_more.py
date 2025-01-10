# Generated by Django 5.1.4 on 2025-01-10 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0024_alter_clinicalchemistry_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicalchemistry',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='crossmatching',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hematology',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rbs',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='serology',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='urinalysis',
            name='re_test',
            field=models.BooleanField(default=False),
        ),
    ]
