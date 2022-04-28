from django import forms
from django.forms.widgets import TextInput, CheckboxInput
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Room
from django.contrib.auth.models import User


class ChatRoomForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = Room
        fields = ['title','users']
        widgets = {
            'title': TextInput(attrs={'class': 'required form-control', 'placeholder': 'New group name'}),
        }
