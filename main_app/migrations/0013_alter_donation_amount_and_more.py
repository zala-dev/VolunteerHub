# Generated by Django 5.0.6 on 2024-07-03 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_volunteeringevent_donation_goal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='volunteeringevent',
            name='donation_goal',
            field=models.PositiveIntegerField(default=0, verbose_name='Donation goal $'),
        ),
    ]
