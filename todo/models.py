from django.db import models
from accounts.models import CustomUser
from datetime import datetime, date, timedelta
from enum import Enum

# Create your models here.
class Goals(models.Model):
    '''目標管理テーブル'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='目標', max_length=50)
    from_date = models.DateField(verbose_name='作成日', auto_now_add=True)
    until_date = models.DateField(verbose_name='期日', null=True, blank=True)
    remind_at = models.TimeField(verbose_name='リマインド時間', null=True, blank=True)
    memo = models.TextField(verbose_name='メモ', null=True, blank=True)
    is_completed = models.BooleanField(verbose_name='完了', default=False)

    def __str__(self):
        return self.subject
    
    @property
    def days_left(self) -> int:
        '''期日までの残り日数を返す'''
        if self.until_date is None:
            return 0
        else:
            return (self.until_date - date.today()).days
        
    @property
    def is_remind(self) -> bool:
        '''リマインド時刻が設定されているかどうか'''
        return bool(self.remind_at)

class TypeChoices(models.TextChoices):
    TASK = 'task', 'なし（タスク）'
    TRAINING = 'training', '回（トレーニング）'
    EXAM = 'exam', '点（テスト）'
    READING = 'reading', 'ページ（読書）'
    SOMETHING = 'something', 'なにか'

class State(Enum):
    '''Todoの状態（Todos.state）'''
    PINNED = 0
    NORMAL = 1
    COMPLETED = 2

class Todos(models.Model):
    '''ToDo管理テーブル'''
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    from_date = models.DateField(verbose_name='作成日', auto_now_add=True)
    until_date = models.DateField(verbose_name='期日', null=True, blank=True)
    image = models.ImageField(verbose_name='画像', null=True, blank=True,
                            upload_to='todo/images/')
    timer = models.IntegerField(verbose_name='タイマー', null=True, blank=True)
    amount = models.IntegerField(verbose_name='合計', null=True, blank=True)
    # タイプ：'task', 'training', 'exam', 'reading'
    type = models.CharField(verbose_name='タイプ', default='task', max_length=20,
                            choices=TypeChoices.choices)
    current = models.IntegerField(verbose_name='進捗', default=0)
    memo = models.TextField(verbose_name='メモ', null=True, blank=True)
    # 状態：ピン留めなら０、通常は１、完了済みは２
    state = models.IntegerField(verbose_name='状態', default=State.NORMAL.value)

    def __str__(self) -> str:
        return self.title
    
    @property
    def unit(self) -> str:
        '''タイプに合わせた単位を返す'''
        if self.type == 'task':
            return ''
        elif self.type == 'training':
            return '回'
        elif self.type == 'exam':
            return '点'
        elif self.type == 'reading':
            return 'ページ'
        else:
            return ''
        
    @property
    def activity(self) -> str:
        '''タイプに合わせた単位を返す'''
        if self.type == 'task':
            return ''
        elif self.type == 'training':
            return '回やった'
        elif self.type == 'exam':
            return '点取れた'
        elif self.type == 'reading':
            return 'ページまで読んだ'
        else:
            return ''
    
    @property
    def is_pinned(self) -> bool:
        '''ピン留めされているかどうか'''
        return State(self.state) == State.PINNED
    
    @property
    def is_completed(self) -> bool:
        '''完了済みかどうか'''
        return State(self.state) == State.COMPLETED
    
    @property
    def days_left(self) -> int:
        '''期日までの残り日数を返す'''
        if self.until_date is None:
            return 0
        else:
            return (self.until_date - date.today()).days
    
    @property
    def percent(self) -> float | None:
        '''進捗率を浮動小数点で返す'''
        if not self.amount:
            return None
        else:
            return self.current / self.amount * 100

class Records(models.Model):
    '''実施記録テーブル'''
    todo = models.ForeignKey(Todos, on_delete=models.CASCADE)
    done_at = models.DateTimeField(verbose_name='日時', auto_now_add=True)
    num = models.IntegerField(verbose_name='数量', null=True, blank=True)
    memo = models.TextField(verbose_name='メモ', null=True, blank=True, max_length=200)

    def __str__(self) -> str:
        return self.todo.title + ' ' + str(self.done_at) + ' ' + str(self.num) + self.todo.unit
