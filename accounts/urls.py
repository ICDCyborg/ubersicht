from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    # ログインページの表示
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # ログアウト
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('user_change/<int:pk>/', views.UserChangeView.as_view(), name='user_change'),
    path('user_change_done/', views.UserChangeDoneView.as_view(), name='user_change_done'),
]
