from django.contrib import admin
from .models import SaaSApp, SubscriptionPlan, UserSubscription, Invoice

# Register the SaaSApp model
class SaaSAppAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

admin.site.register(SaaSApp, SaaSAppAdmin)

# Register the SubscriptionPlan model
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'app', 'price', 'duration_months', 'created_at')
    search_fields = ('name', 'app__name')  # Searching by SaaS app name
    list_filter = ('app', 'duration_months')

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)

# Register the UserSubscription model
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'payment_status')
    search_fields = ('user__email', 'plan__name', 'plan__app__name')
    list_filter = ('plan', 'is_active', 'payment_status')

admin.site.register(UserSubscription, UserSubscriptionAdmin)


# Register the Invoice model with admin
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'subscription', 'total_amount', 'payment_status', 'payment_method', 'payment_date', 'created_at')
    search_fields = ('invoice_number', 'user__email', 'subscription__plan__name', 'payment_method')
    list_filter = ('payment_status', 'payment_method')  # Allow filtering by payment method

admin.site.register(Invoice, InvoiceAdmin)