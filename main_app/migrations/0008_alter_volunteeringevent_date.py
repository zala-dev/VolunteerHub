# Generated by Django 5.0.6 on 2024-06-17 22:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_volunteeringevent_volunteers_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteeringevent',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
