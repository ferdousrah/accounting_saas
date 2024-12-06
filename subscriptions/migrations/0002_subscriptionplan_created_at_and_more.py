# Generated by Django 5.1.4 on 2024-12-06 12:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionplan",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="subscriptionplan",
            name="description",
            field=models.TextField(default="No description available"),
        ),
    ]
