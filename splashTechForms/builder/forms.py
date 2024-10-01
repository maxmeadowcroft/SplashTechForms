# builder/forms.py

from django import forms
from .models import Form


class CreateFormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']
