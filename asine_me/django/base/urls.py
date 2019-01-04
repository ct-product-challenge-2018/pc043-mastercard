from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="asineme_home"),
    path('contact/', views.contact, name="contact"),
    path('welcome/', views.welcome, name="welcome"),
]