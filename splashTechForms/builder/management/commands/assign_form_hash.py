# builder/management/commands/assign_form_hash.py

import hashlib
from django.core.management.base import BaseCommand
from builder.models import Form

class Command(BaseCommand):
    help = 'Assign longer hashes to forms that do not have a hash'

    def handle(self, *args, **kwargs):
        forms_without_hash = Form.objects.filter(form_hash__isnull=True)
        for form in forms_without_hash:
            # Generate a longer unique hash
            form.form_hash = hashlib.sha256(f"{form.title}{form.created_at}".encode('utf-8')).hexdigest()[:16]
            form.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned longer hash to form "{form.title}": {form.form_hash}'))
