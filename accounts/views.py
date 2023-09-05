from typing import Any, Dict
from django.views.generic import CreateView, TemplateView \
    , UpdateView, DeleteView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    '''ユーザ登録ページのビュー'''
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド'''
        # フィールドの値をデータベースに保存
        user = form.save()
        self.object = user
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    '''ユーザ登録完了ページのビュー'''
    template_name = 'signup_success.html'


# need login
@method_decorator(login_required, name='dispatch')
class UserChangeView(UpdateView):
    '''ユーザ情報変更ページのビュー'''
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_config.html'
    success_url = reverse_lazy('accounts:user_change_done')

    def form_valid(self, form):
        form.update(user=self.request.user)
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        user = self.request.user
        if user.pk == self.kwargs['pk']:
            return user
        else:
            from django.http import Http404
            raise Http404('ユーザー情報への編集権限がありません。')
        
@method_decorator(login_required, name='dispatch')
class UserChangeDoneView(TemplateView):
    '''ユーザ情報変更完了ページ'''
    template_name = 'user_config_done.html'

@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    '''ユーザ削除ページ'''
    model = CustomUser
    template_name = 'user_delete.html'
    success_url = reverse_lazy('accounts:user_delete_done')

    def get_object(self, queryset=None):
        user = self.request.user
        if user.pk == self.kwargs['pk']:
            return user
        else:
            from django.http import Http404
            raise Http404('ユーザを削除する権限がありません。')
        
class UserDeleteDoneView(TemplateView):
    '''ユーザ削除完了ページ'''
    template_name = 'user_delete_done.html'