from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserSubscription, SubscriptionPlan, SaaSApp, Invoice
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import SignupForm
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.utils.text import slugify
from django.db import IntegrityError

# Set your Stripe secret key
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# View to display subscription plans
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})

# Signup view to collect user information and start the payment process
def signup(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Get form cleaned data
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            # Generate a unique username, for example by using the email
            username = email.split('@')[0]  # or create a more unique username if needed
            unique_username = username
            counter = 1
            while User.objects.filter(username=unique_username).exists():
                unique_username = f"{username}{counter}"
                counter += 1

            # Create the user
            user = User.objects.create_user(
                username=unique_username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.phone_number = phone_number  # Add phone number
            user.save()

            # Calculate the end date by adding months to the current date
            end_date = timezone.now() + relativedelta(months=plan.duration_months)

            # Create a UserSubscription for the user
            subscription = UserSubscription.objects.create(
                user=user,
                plan=plan,
                end_date=end_date,
                payment_status='pending',
                stripe_subscription_id=None,  # We'll add the stripe subscription ID later
            )

            # Call Stripe to create a checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': plan.name,
                            },
                            'unit_amount': int(plan.price * 100),  # Amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(f'/success/?subscription_id={subscription.id}'),
                cancel_url=request.build_absolute_uri('/cancel/'),
                metadata={'subscription_plan_id': plan.id, 'user_email': email},
            )

            # Redirect user to Stripe Checkout
            return redirect(checkout_session.url, code=303)

    else:
        form = SignupForm()

    return render(request, 'subscriptions/signup.html', {'form': form, 'plan': plan})

# Success view after payment is confirmed
def success(request):
    subscription_id = request.GET.get('subscription_id')
    subscription = get_object_or_404(UserSubscription, id=subscription_id)

    # Update the subscription status to 'paid'
    subscription.payment_status = 'paid'

    # Simulate tenant creation (static values for now)
    tenant_info = {
        'tenant_id': 'tenant_12345',  # Static for now
        'access_url': 'https://accounting-app.example.com/tenant/tenant_12345'
    }

    # Update subscription with tenant ID
    subscription.tenant_id = tenant_info['tenant_id']
    subscription.save()

    # Create an Invoice
    invoice = Invoice.objects.create(
        user=subscription.user,
        subscription=subscription,
        total_amount=subscription.plan.price,
        payment_status="paid",
        payment_method="stripe",  # Static payment method for now
        payment_date=timezone.now(),
    )

    # Send email with access details
    send_mail(
        'Subscription Confirmed',
        f"Dear {subscription.user.first_name},\n\nYour subscription to {subscription.plan.app.name} ({subscription.plan.name}) has been confirmed.\n\n"
        f"Tenant ID: {tenant_info['tenant_id']}\nAccess your accounting app: {tenant_info['access_url']}\n\nInvoice Details:\n"
        f"Invoice Number: {invoice.invoice_number}\nAmount: ${invoice.total_amount}\nPayment Method: {invoice.payment_method.capitalize()}\nPayment Date: {invoice.payment_date.strftime('%Y-%m-%d %H:%M:%S')}",
        settings.DEFAULT_FROM_EMAIL,
        [subscription.user.email],
    )

    return render(request, 'subscriptions/success.html', {'invoice': invoice, 'tenant_info': tenant_info})

# Cancel view for when payment is canceled
def cancel(request):
    return render(request, 'subscriptions/cancel.html')
