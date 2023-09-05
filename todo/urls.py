from django.urls import path
from .views import IndexView, MainView

app_name = 'todo'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('main/', MainView.as_view(), name='main'),
]
