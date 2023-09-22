from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, \
    CreateView, DeleteView, DetailView
from django.views.generic.base import ContextMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# import reverse_lazy
from django.urls import reverse_lazy
# import redirect
from django.shortcuts import redirect

from datetime import date, datetime, timedelta

from . import forms
from .models import Goals, Todos, Records, State, JournalLine, TypeChoices

# Create your views here.
def get_goal(user) -> Optional[Goals]:
    '''目標を取得する'''
    if user.is_anonymous:
        return None
    goal = Goals.objects.filter(user=user, is_completed=False)
    if goal.exists():
        return goal[0]
    else:
        return None
    
class Note:
    '''
    アプリからの通知を表示するカード

    Attributes:
        title: タイトル
        content: 本文
        type: 通知の種類
        button: ボタンに表示する文字列
        link: ボタンを押した際のリンク先
    '''
    def __init__(self, title: str, content: str, type: str='notification',
                button: str='', link:str=''):
        self.title = title
        self.content = content
        self.type = type
        self.button = button
        self.link = link
        return

class GetGoal(ContextMixin):
    '''contextにgoalをセットする基底クラス'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = get_goal(self.request.user)
        return context

class IndexView(TemplateView):
    '''ウェルカムページを表示'''
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class MainView(GetGoal, ListView):
    '''メインページの表示'''
    template_name = 'dashboard.html'
    model = Todos
    
    def get_queryset(self):
        goal = get_goal(self.request.user)
        queryset = Todos.objects.filter(goal=goal).order_by('state')
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        goal = get_goal(self.request.user)
        active_todos = None
        if goal:
            active_todos = Todos.objects.filter(goal=goal).exclude(state=State.COMPLETED.value)
        if not goal:
            if Goals.objects.filter(user=self.request.user).exists():
                context['note'] = Note('目標未設定', '目標が設定されていません。', 
                            button='目標を設定', link=reverse_lazy('todo:goal_config'))
            else:
                context['note'] = Note('目標未設定', '初めての目標を設定しましょう。\n'
                                    '最初は1週間～1か月程度で達成できる、小さな目標がおすすめです。\n\n'
                                    '例：\n'
                                    '・〇〇の資格を取る\n'
                                    '・ダイエットする\n'
                                    '・曲を演奏できるようになる\n'
                                    '・プログラミングを勉強する\n'
                                    '　　　……等', 
                            button='目標を設定', link=reverse_lazy('todo:goal_config'))
        elif goal.until_date == date.today():
            context['note'] = Note('今日が目標の期日です！', '結果はどうだったでしょうか？\n'
                                   '目標達成なら下のボタンを押してください！\n'
                                   '目標未達成の場合は、左の「目標設定」から目標と期日の再設定ができます。', 
                            button='目標達成！', link=reverse_lazy('todo:goal_achieved'))
        elif goal.until_date < date.today():
            context['note'] = Note('目標の期日が過ぎています！', '結果はどうだったでしょうか？\n'
                                   '目標達成なら下のボタンを押してください！\n'
                                   '目標未達成の場合は、左の「目標設定」から目標と期日の再設定ができます。', 
                            button='目標達成！', link=reverse_lazy('todo:goal_achieved'))
        elif not active_todos:
            context['note'] = Note('タスク未設定', '現在のタスクがありません。\nまずは指標を設定してみませんか？\n'
                                'テストなら模試、ダイエットなら体重測定など、自分の現在地を定期的に知ることが大事です。',
                                button='指標を追加', link=reverse_lazy('todo:todo_create', kwargs={'type':'exam'}))
        context['today'] = date.today()
        return context

@method_decorator(login_required, name='dispatch')
class GoalConfigView(GetGoal, UpdateView):
    '''目標設定と更新を行う'''
    template_name = 'goal_config.html'
    form_class = forms.GoalForm
    success_url = reverse_lazy('todo:main')

    def form_valid(self, form):
        from . import mail
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        print(postdata.remind_at)
        if postdata.remind_at:
            mail.MailScheduler.schedule_email_start(self.request.user.pk)
        else:
            mail.MailScheduler.schedule_email_stop(self.request.user.pk)
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return get_goal(self.request.user)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['update'] = bool(get_goal(self.request.user))
        return context
    
@method_decorator(login_required, name='dispatch')
class GoalAchievedView(GetGoal, TemplateView):
    '''目標達成ページ'''
    template_name = 'accomplishment.html'

    def get(self, request, *args, **kwargs):
        try:
            goal = Goals.objects.get(user=request.user, is_completed=False)
            goal.is_completed = True
            goal.save()
            if goal.remind_at:
                from . import mail
                mail.MailScheduler.schedule_email_stop(request.user.pk)
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
        goal = get_goal(request.user)
        if goal:
            goal.delete()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '目標の削除'
        context['message'] = '目標を削除しました。'
        return context

@method_decorator(login_required, name='dispatch')
class AchievementView(GetGoal, ListView):
    '''目標達成実績ページのビュー'''
    template_name = 'achievement.html'
    model = Goals

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Goals.objects.filter(user=self.request.user, is_completed=True)
        for goal in queryset:
            todos = Todos.objects.filter(goal=goal)
            goal.todos = todos
        return queryset

class TodoFormBaseView(GetGoal):
    '''TodoFormを使うベースクラス'''
    template_name = 'todo_config.html'
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
        postdata.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TodoConfigView(TodoFormBaseView, UpdateView):
    '''Todo更新ページ'''

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

    def get_object(self, queryset = ...):
        # typeの数値をCustomChoiceWidgetのデータに変換する
        return Todos.objects.get(pk=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class TodoCreateView(TodoFormBaseView, CreateView):
    '''Todo作成ページ'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'type' in self.kwargs:
            slug = self.kwargs['type']
            if slug in TypeChoices:
                context['type'] = TypeChoices(slug)
        return context

@method_decorator(login_required, name='dispatch')
class TodoCompleteView(GetGoal, TemplateView):
    '''Todoを完了済みにする'''
    template_name = 'accomplishment.html'

    def get(self, request, *args, **kwargs):
        todo = Todos.objects.get(pk=self.kwargs['pk'])
        todo.state = State.COMPLETED.value
        todo.until_date = date.today()
        todo.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = 'タスク完了'
        context['congrats'] = 'タスクを完了し、目標に近づきました！'
        return context


@method_decorator(login_required, name='dispatch')
class TodoDeleteView(GetGoal, TemplateView):
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
class TodoDetailView(GetGoal, DetailView):
    '''Todoの詳細表示'''
    template_name = 'card.html'
    model = Todos
    context_object_name = 'todo'

    def get(self, request, *args, **kwargs):

        # todoの紐づけ
        todo_id = request.GET.get('todo')
        if not todo_id:
            return super().get(request, *args, **kwargs)
        todo = Todos.objects.get(pk=todo_id)
        # numの値を取得
        num = int(request.GET.get('num'))
        memo = request.GET.get('memo')
        # タスクの種類によって処理を変える
        if todo.type == 'training':
            # trainingの場合は加算 
            todo.current += num
        elif todo.type == 'exam' or todo.type == 'reading':
            # examとreadingの場合は値を上書き
            todo.current = num

        record = Records(todo=todo, num=num, memo=memo)
        record.save()
        todo.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        from . import graph
        # グラフの取得
        # 今日から数えて七日前までのデータを一日ごとに集計する。
        # 累計データの場合、累計グラフにする。
        records = Records.objects.filter(todo=self.kwargs['pk'])
        qs = records.filter(done_at__gte=datetime.now() - timedelta(days=7))
        # 一週間のデータがない場合、chart_no_dataをcontextに追加して戻す
        if not qs:
            context = super().get_context_data(**kwargs)
            context['chart_no_data'] = True
            return context
        x = [date.today() - timedelta(days=dy) for dy in range(6, -1, -1)]
        y = []
        if self.object.type == 'training':
            # currentから一日分ずつ引き算することでグラフの値を算出
            y.append(self.object.current)
            for day in reversed(x):
                dx = qs.filter(done_at__date=day).aggregate(models.Sum('num'))['num__sum']
                if dx is None:
                    y.append(y[-1])
                    y[-2] = 0
                else:
                    y.append(y[-1]-dx)
            y.pop()
            y.reverse()
        elif self.object.type == 'exam' or self.object.type == 'reading':
            for day in x:
                try:
                    dx = qs.filter(done_at__date=day).latest('done_at').num
                except Records.DoesNotExist:
                    dx = 0
                y.append(dx)
        x_tick = [day.strftime('%m/%d') for day in x]
        chart = graph.Plot_Graph(x_tick,y, self.object.amount)

        context = super().get_context_data(**kwargs)
        context['chart'] = chart
        context['records'] = records.order_by('-done_at')
        context['today'] = date.today()
        if self.request.GET.get('todo'):
            context['confetti'] = True
        return context

@method_decorator(login_required, name='dispatch')
class RecordView(GetGoal, DetailView):
    '''実施記録の作成'''
    template_name = 'record.html'
    model = Todos
    context_object_name = 'todo'

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
    return redirect('todo:todo_detail', pk=record.todo.pk)

@login_required
def pin_todo(request, pk):
    '''Todoのピン状態を切り替える'''
    todo = Todos.objects.get(pk=pk)
    if todo.state == State.PINNED.value:
        todo.state = State.NORMAL.value
    elif todo.state == State.NORMAL.value:
        todo.state = State.PINNED.value
    todo.save()
    return redirect('todo:main')

class JournalView(GetGoal, TemplateView):
    template_name = 'journal.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            goal = Goals.objects.get(user=self.request.user, is_completed=False)
        except Goals.DoesNotExist:
            return context
        todos = Todos.objects.filter(goal=goal)
        records = Records.objects.filter(todo__in=todos)
        journals = []
        # 記録の行
        for record in records:
            journals.append(JournalLine(record, "record", record.done_at.date()))
        # タスクの行
        for todo in todos:
            journals.append(JournalLine(todo, "todo_start", todo.from_date))
            journals.append(JournalLine(todo, "todo_end", todo.until_date))
        # 目標の行
        journals.append(JournalLine(goal, "goal_start", goal.from_date))
        journals.append(JournalLine(goal, "goal_end", goal.until_date))
        # 日付順に並べ替え
        journals.sort(key=lambda x: x.date, reverse=True)
        object_list = []
        temp_list = []
        # 同じ日付の行は同じメモにつき1行
        for j in journals:
            if len(temp_list) == 0:
                temp_list.append(j)
                continue
            if j.date == temp_list[-1].date:
                temp_list.append(j)
                continue
            object_list.append(temp_list)
            temp_list = [j]
        object_list.append(temp_list)
        context['object_list'] = object_list
        context['today'] = date.today()
        return context