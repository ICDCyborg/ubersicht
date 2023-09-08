from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, \
    CreateView, DeleteView, DetailView
# import methoddecorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# import reverse_lazy
from django.urls import reverse_lazy
# import redirect from django lib
from django.shortcuts import redirect

from . import forms
from .models import Goals, Todos, Records, State

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
            return Todos.objects.filter(goal_id=goal[0].pk).order_by('state')
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

class TodoFormBaseView:
    '''TodoFormを使うベースクラス'''
    template_name = 'todo_config.html'
    form_class = forms.TodoForm
    success_url = reverse_lazy('todo:main')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # 現在のgoalの情報をcontextに埋め込む
        context = super().get_context_data(**kwargs)
        goal = Goals.objects.get(user=self.request.user, is_completed=False)
        context['goal'] = goal
        return context

    def form_valid(self, form):
        postdata = form.save(commit=False)
        # 現在のgoalを取得して紐づける
        try:
            goal = Goals.objects.get(user=self.request.user, is_completed=False)
            postdata.goal = goal
        except Goals.DoesNotExist:
            return super().form_invalid(form)
        postdata.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TodoConfigView(TodoFormBaseView, UpdateView):
    '''Todo更新ページ'''

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

    def get_object(self, queryset: QuerySet[Any] | None = ...):
        # typeの数値をCustomChoiceWidgetのデータに変換する
        return Todos.objects.get(pk=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class TodoCreateView(TodoFormBaseView, CreateView):
    '''Todo作成ページ'''
    ...

@method_decorator(login_required, name='dispatch')
class TodoCompleteView(TemplateView):
    '''Todoを完了済みにする'''
    template_name = 'accomplishment.html'

    def get(self, request, *args, **kwargs):
        todo = Todos.objects.get(pk=self.kwargs['pk'])
        todo.state = State.COMPLETED.value
        todo.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'タスク完了'
        context['congrats'] = 'タスクを完了し、目標に近づきました！'
        return context

@method_decorator(login_required, name='dispatch')
class TodoDeleteView(TemplateView):
    '''Todoを削除する'''
    template_name = 'done.html'

    def get(self, request, *args, **kwargs):
        todo = Todos.objects.get(pk=self.kwargs['pk'])
        todo.delete()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'タスクの削除'
        context['message'] = 'タスクを削除しました。'
        return context

@method_decorator(login_required, name='dispatch')
class TodoDetailView(DetailView):
    '''Todoの詳細表示'''
    template_name = 'todo_detail.html'
    model = Todos
    context_object_name = 'todo'

@method_decorator(login_required, name='dispatch')
class RecordView(DetailView):
    '''実施記録の作成'''
    template_name = 'record.html'
    model = Todos
    context_object_name = 'todo'

@method_decorator(login_required, name='dispatch')
class RecordAddView(TemplateView):
    '''記録追加完了'''
    template_name = 'accomplishment.html'

    def get(self, request, *args, **kwargs):
        # todoの紐づけ
        todo_id = request.GET.get('todo')
        todo = Todos.objects.get(pk=todo_id)
        # numの値を取得
        num = int(request.GET.get('num'))
        # タスクの種類によって処理を変える
        if todo.type == 'training':
            # trainingの場合は加算 
            todo.current += num
        elif todo.type == 'exam' or todo.type == 'reading':
            # examとreadingの場合は値を上書き
            todo.current = num

        record = Records(todo=todo, num=num)
        record.save()
        todo.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '実施記録の追加完了'
        context['congrats'] = '目標に一歩近づきました！'
        return context

@method_decorator(login_required, name='dispatch')
class RecordListView(ListView):
    '''記録の一覧ページ'''
    template_name = 'record_list.html'
    model = Records
    context_object_name = 'records'

    def get_queryset(self) -> QuerySet[Any]:
        todo=Todos.objects.get(pk=self.kwargs['pk'])
        return Records.objects.filter(todo=todo)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['todo'] = Todos.objects.get(pk=self.kwargs['pk'])
        return context

@login_required
def record_delete(request, pk):
    '''実施記録の削除'''
    record = Records.objects.get(pk=pk)
    # Todoのcurrentの値を更新
    todo = record.todo
    if todo.type == 'training':
        todo.current -= record.num
        todo.save()
    elif todo.type == 'exam' or todo.type == 'reading':
        latest_record = Records.objects.filter(todo=todo).exclude(pk=record.pk).latest('done_at')
        todo.current = latest_record.num
        todo.save()
    record.delete()
    return redirect('todo:record_list', pk=record.todo.pk)

@login_required
def pin_todo(request, pk):
    '''Todoのピン状態を切り替える'''
    todo = Todos.objects.get(pk=pk)
    print('pin!'+todo.title+str(todo.state))
    if todo.state == State.PINNED.value:
        todo.state = State.NORMAL.value
    elif todo.state == State.NORMAL.value:
        todo.state = State.PINNED.value
    print('pin!!!'+todo.title+str(todo.state))
    todo.save()
    return redirect('todo:main')