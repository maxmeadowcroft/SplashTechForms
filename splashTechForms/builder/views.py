from .forms import CreateFormForm, AddFieldForm, EditFieldForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, FormField, FieldOption, FormSubmission
from django.contrib.auth.decorators import login_required


# Public form fill-out view
def fill_form_view(request, form_hash):
    form_instance = get_object_or_404(Form, form_hash=form_hash)

    if request.method == 'POST':
        submission_data = {}
        for field in form_instance.fields.all():
            submission_data[field.label] = request.POST.get(field.label)

        # Save the submission data (as JSON)
        FormSubmission.objects.create(form=form_instance, submission_data=submission_data)
        return redirect('form_thank_you')

    return render(request, 'builder/fill_form.html', {'form': form_instance})


# Thank you page after submission
def form_thank_you_view(request):
    return render(request, 'builder/thank_you.html')


@login_required
def dashboard_view(request):
    forms = Form.objects.filter(creator=request.user)
    return render(request, 'builder/dashboard.html', {'forms': forms})


@login_required
def create_or_edit_form_view(request, form_hash=None):
    if form_hash:
        form_instance = get_object_or_404(Form, form_hash=form_hash, creator=request.user)
    else:
        form_instance = None

    if request.method == 'POST':
        form = CreateFormForm(request.POST, instance=form_instance)
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.creator = request.user
            saved_form.save()
            # Redirect to manage fields using form_hash
            return redirect('manage_fields', form_hash=saved_form.form_hash)
    else:
        form = CreateFormForm(instance=form_instance)

    return render(request, 'builder/create_edit_form.html', {'form': form})


@login_required
def manage_fields_view(request, form_hash):
    form_instance = get_object_or_404(Form, form_hash=form_hash, creator=request.user)
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
    form_hash = field.form.form_hash
    field.delete()
    return redirect('manage_fields', form_hash=form_hash)


@login_required
def edit_field_view(request, field_id):
    field_instance = get_object_or_404(FormField, id=field_id, form__creator=request.user)

    if request.method == 'POST':
        edit_form = EditFieldForm(request.POST, instance=field_instance)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('manage_fields', form_hash=field_instance.form.form_hash)  # Redirect back to form's fields
    else:
        edit_form = EditFieldForm(instance=field_instance)

    return render(request, 'builder/edit_field.html', {
        'edit_form': edit_form,
        'field': field_instance
    })


@login_required
def add_field_options_view(request, field_id):
    field_instance = get_object_or_404(FormField, id=field_id, form__creator=request.user)

    if request.method == 'POST':
        option_value = request.POST.get('option_value')
        if option_value:
            FieldOption.objects.create(form_field=field_instance, value=option_value)
        return redirect('add_field_options', field_id=field_instance.id)

    return render(request, 'builder/add_field_options.html', {'field': field_instance})


@login_required
def delete_form_view(request, form_hash):
    form_instance = get_object_or_404(Form, form_hash=form_hash, creator=request.user)
    form_instance.delete()
    return redirect('dashboard')


@login_required
def view_responses(request, form_hash):
    form_instance = get_object_or_404(Form, form_hash=form_hash, creator=request.user)
    responses = FormSubmission.objects.filter(form=form_instance)
    return render(request, 'builder/view_responses.html', {'form': form_instance, 'responses': responses})


@login_required
def delete_field_option_view(request, option_id):
    option = get_object_or_404(FieldOption, id=option_id, form_field__form__creator=request.user)
    form_hash = option.form_field.form.form_hash
    option.delete()
    return redirect('add_field_options', field_id=option.form_field.id)
