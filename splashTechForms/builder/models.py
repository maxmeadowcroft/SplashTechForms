# builder/models.py

from django.db import models
from django.contrib.auth.models import User

class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # You can add more fields like form structure here

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/form/{self.id}/"

class FormSubmission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    submission_data = models.JSONField()  # Store form data as JSON
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.form.title} on {self.submitted_at}"
