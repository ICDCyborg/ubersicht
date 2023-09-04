from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

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