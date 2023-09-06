from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView
# import methoddecorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import GoalsForm

# import reverse_lazy
from django.urls import reverse_lazy

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
        goal = Goals.objects.filter(user_id=self.request.user.pk, is_completed = False)
        return Todos.objects.filter(goal_id=goal[0].pk)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['goal'] = Goals.objects.filter(user_id=self.request.user.pk, is_completed = False)[0]
        return context

@method_decorator(login_required, name='dispatch')
class GoalConfigView(UpdateView):
    '''目標設定を行う'''
    template_name = 'goal_config.html'
    form_class = GoalsForm
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
    
@method_decorator(login_required, name='dispatch')
class GoalAchievedView(TemplateView):
    '''目標達成ページ'''
    template_name = 'accomplishment.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = '目標達成！'
        context['congrats'] = '目標を達成しました！おめでとうございます！'
        return context