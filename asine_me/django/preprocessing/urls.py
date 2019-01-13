from django.urls import path

from . import views

urlpatterns = [
    path('create_model/', views.createModel, name="create_model"),
    path('data_preprocessing/', views.dataPreprocessing, name="data_preprocessing"),
    path('preprocessing_confirmation/', views.preprocessingConfirmation, name="preprocessing_confirmation"),
    path('model_results/', views.modelResults, name="model_results"),
    # path('loading_page/', views.loadingPage, name="loading_page"),
]