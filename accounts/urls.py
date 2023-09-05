from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # ユーザ登録
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    # ログインページの表示
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # ログアウト
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    # ユーザ情報の変更
    path('user_change/<int:pk>/', views.UserChangeView.as_view(), name='user_change'),
    path('user_change_done/', views.UserChangeDoneView.as_view(), name='user_change_done'),
    # 退会処理
    path('user_delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('user_delete_done/', views.UserDeleteDoneView.as_view(), name='user_delete_done'),

]
