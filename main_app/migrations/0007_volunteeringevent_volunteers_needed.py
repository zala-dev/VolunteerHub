# Generated by Django 5.0.6 on 2024-06-17 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_volunteeringevent_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteeringevent',
            name='volunteers_needed',
            field=models.IntegerField(default=0),
        ),
    ]