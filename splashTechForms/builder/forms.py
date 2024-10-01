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
        fields = ['label', 'field_type', 'required']
        widgets = {
            'field_type': forms.Select(choices=[
                ('text', 'Text Field'),
                ('textarea', 'Text Area'),
                ('radio', 'Radio Buttons'),
                ('checkbox', 'Checkbox'),
                ('select', 'Dropdown'),
                ('date', 'Date Picker'),
            ]),
        }


# Form for adding options to fields (radio buttons, dropdowns)
class AddFieldOptionForm(forms.ModelForm):
    class Meta:
        model = FieldOption
        fields = ['value']


class EditFieldForm(forms.ModelForm):
    class Meta:
        model = FormField
        fields = ['label', 'description', 'field_type', 'required']
