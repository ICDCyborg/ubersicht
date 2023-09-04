from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    '''ウェルカムページを表示するビュー'''
    template_name = 'index.html'