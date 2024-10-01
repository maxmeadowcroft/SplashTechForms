# builder/forms.py

from django import forms
from .models import Form, FormField, FieldOption


class CreateFormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']


# Form to create or edit fields
class AddFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ['label', 'description', 'field_type', 'required']


# Form for adding options to fields (radio buttons, dropdowns)
class AddFieldOptionForm(forms.ModelForm):
    class Meta:
        model = FieldOption
        fields = ['value']


class EditFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ['label', 'description', 'field_type', 'required']
