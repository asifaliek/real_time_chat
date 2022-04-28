from django import forms
from django.forms.widgets import TextInput, CheckboxInput,Select
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Thread
from django.contrib.auth.models import User


class PersonalChatForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)
    class Meta:
        model = Thread
        fields = ['users']
        