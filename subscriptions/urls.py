from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_plans, name='subscription_plans'),
    path('signup/<int:plan_id>/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
