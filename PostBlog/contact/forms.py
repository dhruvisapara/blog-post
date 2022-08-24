from django.forms import ModelForm, forms

from contact.models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields="__all__"
