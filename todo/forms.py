from django.forms import ModelForm
from .models import Goals, Todos, Records
from django import forms

# class CustomSelectWidget(forms.Select):
#     choices = ('なし（タスク）', '回（トレーニング）', '点（テスト）', 'ページ（読書）')

class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ['subject', 'until_date', 'remind_at', 'memo']

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todos
        fields = ['title', 'until_date', 'amount', 'type', 'image', 'timer', 'memo']