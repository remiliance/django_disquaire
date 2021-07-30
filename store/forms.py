from django.forms import ModelForm, TextInput, EmailInput
from store.models import Contact
from django import forms

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email"]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'})
        }

