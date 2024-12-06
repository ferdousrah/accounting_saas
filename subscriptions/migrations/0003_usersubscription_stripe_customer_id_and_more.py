# Generated by Django 5.1.4 on 2024-12-06 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0002_subscriptionplan_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersubscription",
            name="stripe_customer_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="usersubscription",
            name="stripe_subscription_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="usersubscription",
            name="subscription_status",
            field=models.CharField(default="active", max_length=20),
        ),
        migrations.AddField(
            model_name="usersubscription",
            name="tenant_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]