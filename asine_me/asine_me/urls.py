"""asine_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommendations import views as recommendations_views
from preprocessing import views as preprocessing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recommendations_views.home, name="asineme_home"),
    path('welcome/', recommendations_views.welcome, name="welcome"),
    path('input_leads/', recommendations_views.inputNewLeads, name="input_leads"),
    path('recommendations/', recommendations_views.recommendations, name="recommendations"),

    path('create_model/', preprocessing_views.createModel, name="create_model"),
    path('data_preprocessing/', preprocessing_views.dataPreprocessing, name="data_preprocessing"),
    path('preprocessing_confirmation/', preprocessing_views.preprocessingConfirmation, name="preprocessing_confirmation"),
    path('model_results/', preprocessing_views.modelResults, name="model_results"),
    path('loading_page/', preprocessing_views.loadingPage, name="loading_page"),
]
