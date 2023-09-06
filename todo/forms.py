from django.forms import ModelForm
from .models import Goals, Todos, Records
from django import forms

class CustomSelectWidget(forms.Select):
    choices = ('なし（タスク）', '回（トレーニング）', '点（テスト）', 'ページ（読書）')

class GoalsForm(ModelForm):
    class Meta:
        model = Goals
        fields = ['subject', 'until_date', 'remind_at', 'memo']

class TodoForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # from_date = forms.HiddenInput()
    # until_date = forms.DateField(required=False)
    # amount = forms.IntegerField(required=False)
    # type = forms.HiddenInput()
    choice_of_type = forms.ChoiceField(
        choices=list(enumerate(CustomSelectWidget.choices)),
        # choices=(),
        widget=CustomSelectWidget,
        required=True
    )
    # image = forms.ImageField(required=False)
    # timer = forms.IntegerField(required=False)
    # memo = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Todos
        fields = ['title', 'until_date', 'amount', 'choice_of_type', 'image', 'timer', 'memo']