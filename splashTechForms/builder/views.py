# builder/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Form, FormField
from .forms import CreateFormForm, AddFieldForm, EditFieldForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    forms = Form.objects.filter(creator=request.user)
    return render(request, 'builder/dashboard.html', {'forms': forms})

@login_required
def create_or_edit_form_view(request, form_id=None):
    if form_id:
        form_instance = get_object_or_404(Form, id=form_id, creator=request.user)
    else:
        form_instance = None

    if request.method == 'POST':
        form = CreateFormForm(request.POST, instance=form_instance)
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.creator = request.user
            saved_form.save()
            return redirect('manage_fields', saved_form.id)
    else:
        form = CreateFormForm(instance=form_instance)

    return render(request, 'builder/create_edit_form.html', {'form': form})

@login_required
def manage_fields_view(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id, creator=request.user)
    fields = form_instance.fields.all()

    if request.method == 'POST':
        if 'add_field' in request.POST:
            field_form = AddFieldForm(request.POST)
            if field_form.is_valid():
                new_field = field_form.save(commit=False)
                new_field.form = form_instance
                new_field.save()
        elif 'save_form' in request.POST:
            return redirect('dashboard')

    else:
        field_form = AddFieldForm()

    return render(request, 'builder/manage_fields.html', {
        'form': form_instance,
        'fields': fields,
        'field_form': field_form
    })

@login_required
def delete_field_view(request, field_id):
    field = get_object_or_404(FormField, id=field_id, form__creator=request.user)
    form_id = field.form.id
    field.delete()
    return redirect('manage_fields', form_id)


@login_required
def edit_field_view(request, field_id):
    field_instance = get_object_or_404(FormField, id=field_id, form__creator=request.user)

    if request.method == 'POST':
        edit_form = EditFieldForm(request.POST, instance=field_instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('manage_fields', field_instance.form.id)
    else:
        edit_form = EditFieldForm(instance=field_instance)

    return render(request, 'builder/edit_field.html', {
        'edit_form': edit_form,
        'field': field_instance
    })
