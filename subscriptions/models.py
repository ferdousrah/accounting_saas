from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# SaaS App Model
class SaaSApp(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Subscription Plan Model
class SubscriptionPlan(models.Model):
    app = models.ForeignKey(SaaSApp, related_name='subscription_plans', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    description = models.TextField(default="No description available")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.app.name} - {self.name}"

# User Subscription Model
class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending')])
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    subscription_status = models.CharField(max_length=20, default="active")
    tenant_id = models.CharField(max_length=255, null=True, blank=True)  # Simulated tenant ID for now

    def __str__(self):
        return f"{self.user.email} - {self.plan.app.name} - {self.plan.name}"


# Working on invoice

# Define available payment methods
PAYMENT_METHOD_CHOICES = [
    ('paypal', 'PayPal'),
    ('stripe', 'Stripe'),
    ('cash', 'Cash'),
    ('bank_transfer', 'Bank Transfer'),
    ('other', 'Other'),
]


# Invoice model
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    payment_date = models.DateTimeField(default=timezone.now)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure invoice_number is generated before saving
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        # Generate invoice number based on the last invoice
        last_invoice = Invoice.objects.all().order_by('-id').first()
        last_invoice_number = int(last_invoice.invoice_number.split('-')[1]) if last_invoice else 0
        # Return the invoice number with leading zeros, e.g., INV-000001
        return f"INV-{last_invoice_number + 1:06d}"

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.email}"
