from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
# import methoddecorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Goals, Todos, Records
# Create your views here.

class IndexView(TemplateView):
    '''ウェルカムページを表示するビュー'''
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class MainView(ListView):
    template_name = 'main.html'
    model = Todos
    
    def get_queryset(self):
        goal = Goals.objects.filter(user_id=self.request.user.pk, is_completed = False)
        return Todos.objects.filter(goal_id=goal[0].pk)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['goal'] = Goals.objects.filter(user_id=self.request.user.pk, is_completed = False)[0]
        return context
