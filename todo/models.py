from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Goals(models.Model):
    '''目標管理テーブル'''
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='目標', max_length=50)
    from_date = models.DateField(verbose_name='作成日', auto_now_add=True)
    until_date = models.DateField(verbose_name='期日', null=True, blank=True)
    remind_at = models.TimeField(verbose_name='リマインド時間', null=True, blank=True)
    memo = models.TextField(verbose_name='メモ', null=True, blank=True)
    is_completed = models.BooleanField(verbose_name='完了', default=False)

    def __str__(self):
        return self.subject

class Todos(models.Model):
    '''ToDo管理テーブル'''
    goal_id = models.ForeignKey(Goals, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    from_date = models.DateField(verbose_name='作成日', auto_now_add=True)
    until_date = models.DateField(verbose_name='期日', null=True, blank=True)
    image = models.ImageField(verbose_name='画像', null=True, blank=True)
    timer = models.IntegerField(verbose_name='タイマー', null=True, blank=True)
    # タイプ：タスクなら０、トレーニングが１、テストが２、読書が３
    type = models.IntegerField(verbose_name='タイプ', default=0)
    amount = models.IntegerField(verbose_name='合計', null=True, blank=True)
    current = models.IntegerField(verbose_name='進捗', null=True, blank=True)
    memo = models.TextField(verbose_name='メモ', null=True, blank=True)
    # 状態：ピン留めなら０、通常は１、完了済みは２
    state = models.IntegerField(verbose_name='状態', default=1)

    def __str__(self) -> str:
        return self.title

class Records(models.Model):
    '''実施記録テーブル'''
    todo_id = models.ForeignKey(Todos, on_delete=models.CASCADE)
    done_at = models.DateTimeField(verbose_name='日時', auto_now_add=True)
    num = models.IntegerField(verbose_name='数量', null=True, blank=True)

    def __str__(self) -> str:
        return self.todo_id.title + ' ' + str(self.done_at) + ' ' + str(self.num)
