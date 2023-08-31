# UserCreationFormのインポート
from django.contrib.auth.forms import UserCreationForm
# models.pyで定義したCustomUserモデルをインポート
from .models import CustomUser

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