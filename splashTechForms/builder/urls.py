# builder/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('form/<str:form_hash>/fill/', views.fill_form_view, name='fill_form'),
    path('form/create/', views.create_or_edit_form_view, name='create_form'),
    path('form/<str:form_hash>/edit/', views.create_or_edit_form_view, name='edit_form'),
    path('form/<str:form_hash>/fields/', views.manage_fields_view, name='manage_fields'),
    path('form/<str:form_hash>/delete/', views.delete_form_view, name='delete_form'),
    path('form/thank-you/', views.form_thank_you_view, name='form_thank_you'),
    path('form/field/<int:field_id>/edit/', views.edit_field_view, name='edit_field'),
    path('form/field/<int:field_id>/delete/', views.delete_field_view, name='delete_field'),
    path('form/field/<int:field_id>/options/', views.add_field_options_view, name='add_field_options'),
    path('app/form/<str:form_hash>/responses/', views.view_responses, name='view_responses'),
    path('form/field/option/<int:option_id>/delete/', views.delete_field_option_view, name='delete_field_option'),
]
