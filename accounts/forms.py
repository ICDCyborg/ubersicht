# UserCreationFormのインポート
from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# models.pyで定義したCustomUserモデルをインポート
from .models import CustomUser

from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    '''
    UserCreationFormを継承したクラス
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['dream'].label = 'なりたい自分（任意）'
        self.fields['dream'].widget.attrs['placeholder'] = 'あなたはどんな自分になりたいですか？\n目標を達成した後どんな自分になっていると思いますか？\n少し時間をとって考えてみてください。'
        return
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