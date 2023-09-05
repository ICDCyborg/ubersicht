from django.shortcuts import render
from django.views.generic import TemplateView
# import methoddecorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class IndexView(TemplateView):
    '''ウェルカムページを表示するビュー'''
    template_name = 'index.html'

@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = 'main.html'