from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
# import methoddecorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# import reverse_lazy
from django.urls import reverse_lazy

from . import forms
from .models import Goals, Todos, Records
from django.urls import reverse_lazy
# Create your views here.

class IndexView(TemplateView):
    '''ウェルカムページを表示'''
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class MainView(ListView):
    '''メインページの表示'''
    template_name = 'main.html'
    model = Todos
    
    def get_queryset(self):
        goal = Goals.objects.filter(user=self.request.user, is_completed=False)
        if goal.exists():
            return Todos.objects.filter(goal_id=goal[0].pk)
        else:
            return Todos.objects.none()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        goal = Goals.objects.filter(user=self.request.user, is_completed=False)
        if goal.exists():
            context['goal'] = goal[0]
        return context

@method_decorator(login_required, name='dispatch')
class GoalConfigView(UpdateView):
    '''目標設定と更新を行う'''
    template_name = 'goal_config.html'
    form_class = forms.GoalForm
    success_url = reverse_lazy('todo:main')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        active_goal = Goals.objects.filter(user=self.request.user, is_completed=False)
        if active_goal.exists():
            return active_goal[0]
        else:
            return Goals()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        active_goal = Goals.objects.filter(user=self.request.user, is_completed=False)
        context['update'] = active_goal.exists()
        return context
    
@method_decorator(login_required, name='dispatch')
class GoalAchievedView(TemplateView):
    '''目標達成ページ'''
    template_name = 'accomplishment.html'

    def get(self, request, *args, **kwargs):
        try:
            goal = Goals.objects.get(user=request.user, is_completed=False)
            goal.is_completed = True
            goal.save()
        except Goals.DoesNotExist:
            pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '目標達成！'
        context['congrats'] = '目標を達成しました！おめでとうございます！'
        return context

@method_decorator(login_required, name='dispatch')
class GoalDeleteView(TemplateView):
    '''目標の削除を行う'''
    template_name = 'done.html'

    def get(self, request, *args, **kwargs):
        try:
            goal = Goals.objects.get(user=request.user, is_completed=False)
            goal.delete()
        except Goals.DoesNotExist:
            pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '目標の削除'
        context['message'] = '目標を削除しました。'
        return context

@method_decorator(login_required, name='dispatch')
class AchievementView(ListView):
    '''目標達成実績ページのビュー'''
    template_name = 'achievement.html'
    model = Goals

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Goals.objects.filter(user=self.request.user, is_completed=True)
        for goal in queryset:
            todos = Todos.objects.filter(goal=goal)
            goal.todos = todos
        return queryset

@method_decorator(login_required, name='dispatch')
class TodoConfigView(UpdateView):
    '''Todoの作成と更新を行う'''
    template_name = 'todo_config.html'
    # model = Todos
    form_class = forms.TodoForm
    success_url = reverse_lazy('todo:main')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        # 現在のgoalを取得して紐づける
        try:
            goal = Goals.objects.get(user=self.request.user, is_completed=False)
            postdata.goal = goal
        except Goals.DoesNotExist:
            return super().form_invalid(form)
        print('image:'+str(postdata.image))
        postdata.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['goal'] = Todos.objects.get(pk=self.kwargs['pk']).goal
        context['update'] = True
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...):
        # typeの数値をCustomChoiceWidgetのデータに変換する
        return Todos.objects.get(pk=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class TodoCreateView(CreateView):
    template_name = 'todo_config.html'
    form_class = forms.TodoForm
    success_url = reverse_lazy('todo:main')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # 現在のgoalの情報をcontextに埋め込む
        context = super().get_context_data(**kwargs)
        goal = Goals.objects.get(user=self.request.user, is_completed=False)
        context['goal'] = goal
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        postdata = form.save(commit=False)
        # 現在のgoalに紐づける
        try:
            goal = Goals.objects.get(user=self.request.user, is_completed=False)
            postdata.goal = goal
        except Goals.DoesNotExist:
            return super().form_invalid(form)
        postdata.save()
        return super().form_valid(form)