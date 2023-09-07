from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    # ログイン前
    path('', IndexView.as_view(), name='index'),
    # メインページ
    path('main/', MainView.as_view(), name='main'),
    # 目標設定
    path('goal_config/', GoalConfigView.as_view(), name='goal_config'),
    # 目標達成
    path('goal_achieved/', GoalAchievedView.as_view(), name='goal_achieved'),
    path('goal_delete/', GoalDeleteView.as_view(), name='goal_delete'),
    path('achievement/', AchievementView.as_view(), name='achievement'),
    # Todoの作成、編集
    path('todo_create/', TodoCreateView.as_view(), name='todo_create'),
    path('todo_config/<int:pk>', TodoConfigView.as_view(), name='todo_config'),
    path('todo_complete/<int:pk>', TodoCompleteView.as_view(), name='todo_complete'),
    path('todo_delete/<int:pk>', TodoDeleteView.as_view(), name='todo_delete'),
]
