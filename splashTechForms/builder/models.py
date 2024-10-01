# builder/models.py

from django.db import models
from django.contrib.auth.models import User


# Main form model
class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/form/{self.id}/"


# Different types of fields that can be added to forms
FIELD_TYPES = [
    ('text', 'Text Field'),
    ('textarea', 'Text Area'),
    ('radio', 'Radio Buttons'),
    ('checkbox', 'Checkbox'),
    ('select', 'Dropdown'),
]


class FormField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Optional description
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

    def needs_options(self):
        return self.field_type in ['radio', 'select']


class FieldOption(models.Model):
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class FormSubmission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    submission_data = models.JSONField()  # Store the form submission data as JSON
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.form.title} on {self.submitted_at}"
