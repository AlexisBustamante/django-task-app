from django.forms import ModelForm
from .models import Task
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control0', 'placeholder': 'write the title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write the description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center m-auto'})
        }
