from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    # ログイン前
    path('', IndexView.as_view(), name='index'),
    # メインページ
    path('main/', MainView.as_view(), name='main'),
    # 目標設定
    path('goal_config', GoalConfigView.as_view(), name='goal_config'),
    # 目標達成
    path('goal_achieved', GoalAchievedView.as_view(), name='goal_achieved'),

]
