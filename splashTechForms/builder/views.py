from django.shortcuts import render
from .forms import SimpleForm


def form_view(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            # Handle form processing here
            print(form.cleaned_data)
    else:
        form = SimpleForm()

    return render(request, 'builder/form_template.html', {'form': form})
