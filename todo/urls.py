from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    # ログイン前
    path('', IndexView.as_view(), name='index'),
    # メインページ
    path('main/', MainView.as_view(), name='main'),
    # 目標の設定、編集、削除
    path('goal/config/', GoalConfigView.as_view(), name='goal_config'),
    path('goal/achieved/', GoalAchievedView.as_view(), name='goal_achieved'),
    path('goal/delete/', GoalDeleteView.as_view(), name='goal_delete'),
    # 目標の達成実績
    path('achievement/', AchievementView.as_view(), name='achievement'),
    # Todoの作成、閲覧、編集、削除
    path('todo/create/', TodoCreateView.as_view(), name='todo_create'),
    path('todo/create/<slug:type>', TodoCreateView.as_view(), name='todo_create'),
    path('todo/<int:pk>', TodoDetailView.as_view(), name='todo_detail'),
    path('todo/config/<int:pk>', TodoConfigView.as_view(), name='todo_config'),
    path('todo/complete/<int:pk>', TodoCompleteView.as_view(), name='todo_complete'),
    path('todo/delete/<int:pk>', TodoDeleteView.as_view(), name='todo_delete'),
    path('todo/pin/<int:pk>', pin_todo, name='pin'),
    # 実施記録の作成、閲覧、削除
    path('record/delete/<int:pk>', record_delete, name='record_delete'),
    path('journal/', JournalView.as_view(), name='journal'),
    ### 以下はtodo_detailに統合済み ###
    # path('record/add/<int:pk>', RecordView.as_view(), name='record'),
    # path('record/add/done/', RecordAddView.as_view(), name='record_add'),
    # path('record/<int:pk>', RecordListView.as_view(), name='record_list'),
    # path('timer/', TimerView.as_view(), name='timer'),
]
