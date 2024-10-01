# builder/models.py

from django.db import models
from django.contrib.auth.models import User
import hashlib


class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    form_hash = models.CharField(max_length=16, unique=True, blank=True, null=True)  # Increased hash length

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/app/form/{self.form_hash}/fill/"

    def save(self, *args, **kwargs):
        # Generate a unique hash for new forms, using a longer portion of the hash
        if not self.form_hash:
            self.form_hash = hashlib.sha256(f"{self.title}{self.created_at}".encode('utf-8')).hexdigest()[:16]  # Longer hash
        super().save(*args, **kwargs)


# To store different types of fields
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
    description = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

    def needs_options(self):
        return self.field_type in ['radio', 'select']


# Options for fields like radio buttons and dropdowns
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
