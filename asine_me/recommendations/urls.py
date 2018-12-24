from django.urls import path

from . import views

urlpatterns = [
    path('input_leads/', views.inputNewLeads, name="input_leads"),
    path('matches/', views.recommendations, name="recommendations"),
]