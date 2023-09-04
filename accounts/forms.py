# UserCreationFormのインポート
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# models.pyで定義したCustomUserモデルをインポート
from .models import CustomUser

from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    '''
    UserCreationFormを継承したクラス
    '''
    class Meta:
        '''
        UserCreationFormのメタクラス
        
        Attributes:
            model: 連携するユーザーモデル
            fields: 入力するフィールド
        '''
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'dream')

class CustomUserChangeForm(UserChangeForm):
    '''
    UserChangeFormを継承したカスタムフォーム
    '''
    class Meta:
        '''
        UserChangeFormのメタクラス
        
        Attributes:
            model: 連携するモデル
            fields: 入力するフィールド
        '''
        model = CustomUser
        fields = ('username', 'email', 'dream')
    
    def update(self, user):
        '''ユーザ情報の更新'''
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.dream = self.cleaned_data['dream']
        user.save()