# builder/views.py

from django.shortcuts import render, redirect
from .models import Form, FormSubmission
from .forms import CreateFormForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    forms = Form.objects.filter(creator=request.user)
    return render(request, 'builder/dashboard.html', {'forms': forms})

@login_required
def create_form_view(request):
    if request.method == 'POST':
        form = CreateFormForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.creator = request.user
            new_form.save()
            return redirect('dashboard')
    else:
        form = CreateFormForm()
    return render(request, 'builder/create_form.html', {'form': form})

@login_required
def form_data_view(request, form_id):
    form = Form.objects.get(id=form_id, creator=request.user)
    submissions = form.submissions.all()
    return render(request, 'builder/form_data.html', {'form': form, 'submissions': submissions})
