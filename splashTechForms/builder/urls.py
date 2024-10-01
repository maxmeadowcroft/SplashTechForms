# builder/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('form/create/', views.create_form_view, name='create_form'),
    path('form/<int:form_id>/data/', views.form_data_view, name='form_data'),
]
