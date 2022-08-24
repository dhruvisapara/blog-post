from django.shortcuts import render, redirect
from .forms import BookModelFormset


def create_book_model_form(request):
    template_name = 'store1/create_normal.html'
    heading_message = 'Model Formset Demo'
    if request.method == 'GET':
        formset = BookModelFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('name'):
                    form.save()
            return redirect('book_list')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
