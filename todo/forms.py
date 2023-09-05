from django.forms import ModelForm
from .models import Goals, Todos, Records
from django import forms

class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ['subject', 'until_date', 'remind_at', 'memo']
    