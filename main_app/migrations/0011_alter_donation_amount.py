# Generated by Django 5.0.6 on 2024-06-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.PositiveIntegerField(choices=[('0', '$0'), ('20', '$20'), ('50', '$50'), ('100', '$100'), ('200', '$200')], default='0'),
        ),
    ]
