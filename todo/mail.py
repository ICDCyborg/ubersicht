
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.db import models

from apscheduler.schedulers.background import BackgroundScheduler

from datetime import date, timedelta

from accounts.models import CustomUser
from ubersicht.settings import LOGIN_URL
from .models import Goals, Records, Todos, TypeChoices, State

class MailScheduler:
    # ジョブリストを格納する辞書型。{ user.pk : job_id }
    job_dict = {}
    scheduler = BackgroundScheduler()
    ready = False

    def send_email(self, goal):
        '''リマインドメールをユーザに送る'''
        # ガード節
        if goal.is_completed:
            return
        today = date.today()-timedelta(days=1)
        
        to_list = [goal.user.email]
        subject = f'【ubersicht】{today.strftime("%m月%d日")}のリマインド'

        #### メール本文 ####
        # 呼びかけ
        body = f'{goal.user.username}さん\n'

        # 目標の期限に対応した一言挨拶
        if goal.until_date is not None:
            if goal.days_left == 0:
                body += '今日が目標の期日でしたね！\n結果はどうでしたか？\n'
                body += 'ぜひログインして、結果を教えてください！\n'
                body += reverse_lazy(LOGIN_URL) + '\n'
            elif goal.days_left == 1:
                body += '明日が目標の期日ですね！準備は万全ですか？\n頑張ってください！\n'
            elif goal.days_left <= 0:
                body += '目標の期日が過ぎているようです。\n結果はどうでしたか？\n'
                body += 'ぜひログインして、結果を教えてください！\n'
                body += reverse_lazy(LOGIN_URL) + '\n'
            else:
                body += f'目標まであと{goal.days_left}日ですね。\n'
                body += '一歩ずつ進んでいきましょう！\n\n'

        # 本日の進捗（記録）
        todo_list = Todos.objects.filter(goal=goal)
        records = Records.objects.filter(todo__in=todo_list, done_at__date=today)
        todos = []
        for record in records:
            if record.todo not in todos:
                todos.append(record.todo)
        if todos:
            body += "\n今日の進捗：\n"
        for todo in todos:
            body += f'●{todo.title}...'
            if todo.type == TypeChoices.TRAINING.value:
                progress = records.aggregate(sum=models.Sum('num'))['sum']
            elif todo.type == TypeChoices.EXAM.value \
                or todo.type == TypeChoices.READING.value:
                progress = records.latest('done_at').num
            body += f'{progress}{todo.activity}\n'
        # 本日の進捗（完了したタスク）
        comp_todos = Todos.objects.filter(goal=goal, state=State.COMPLETED.value,
                                        until_date=today)
        if not todos and comp_todos:
            body += "\n今日の進捗：\n"
        for todo in comp_todos:
            body += f'●{todo.title}...完了！\n'
        
        # 明日の予定（明日が期限のタスク）
        active_todos = Todos.objects.filter(goal=goal).exclude(state=State.COMPLETED.value)
        tommorow_todos = active_todos.filter(until_date=today+timedelta(days=1))
        # 未完了のTodoが無い
        if not active_todos.exists():
            body += '\nやる事が設定されていません。\n'
        # 明日終了予定の未完了のTodoが無い
        elif not tommorow_todos.exists():
            nearest_todo = active_todos.order_by('until_date')[0]
            if nearest_todo.until_date is not None:
                # 期限が設定された予定がある
                body += f'\n{nearest_todo.until_date:%#m月%#d日}の予定：\n●{nearest_todo.title}\n'
            else:
                body += f'\n未完了の予定：\n●{nearest_todo.title}\n'
        # 明日終了予定の未完了のTodoが有る
        else:
            body += '\n明日の予定：\n'
            for todo in tommorow_todos:
                body += f'●{todo.title}\n'

        # 期限切れのタスク
        expired_todos = active_todos.filter(until_date__lt=today)
        if expired_todos.exists():
            body += '\n期限切れの予定：\n'
            for todo in expired_todos:
                body += f'●{todo.title}...{todo.until_date:%#m月%#d日}まで\n'
            body += '※既に完了していますか？ログインして完了済みにして下さい。'

        # 明日も頑張りましょう！
        body += '\n今日も一日お疲れさまでした！\n明日も頑張っていきましょう。\n'

        # クレジット、リンク
        body += '\n----------------\n'
        body += 'copyright ubersicht 2023 all rights reserved.\n'

        email = EmailMessage(subject, body, to=to_list)
        email.send()
        print('メール送信：'+str(to_list))

    @classmethod
    def schedule_email_init(self):
        '''目標リストを参照し、リマインドメールの時刻をまとめて設定する'''
        print('initializing....')
        # メール送信設定した目標のユーザを全て抜き出す
        queryset = Goals.objects.filter(remind_at__isnull=False, is_completed=False)
        for goal in queryset:
            if goal.user.pk in self.job_dict:
                continue
            hour = goal.remind_at.hour
            minute = goal.remind_at.minute
            job_id = self.scheduler.add_job(self.send_email, 'cron', hour=hour, minute=minute, args=[self, goal]).id
            self.job_dict[goal.user.pk] = job_id
            print('registered job for '+goal.user.username)

    @classmethod
    def schedule_email_stop(self, user_id: int):
        '''user_idで指定されたユーザへのメールを停止する'''
        if user_id not in self.job_dict:
            return
        user = CustomUser.objects.get(pk=user_id)
        self.scheduler.remove_job(self.job_dict[user_id])
        del self.job_dict[user_id]
        print('unregistered job for '+user.username)

    @classmethod
    def schedule_email_start(self, user_id: int):
        '''user_idで指定されたユーザのメールを開始する'''
        if user_id in self.job_dict:
            self.schedule_email_stop(user_id)
        user = CustomUser.objects.get(pk=user_id)
        goal = Goals.objects.get(user=user, is_completed=False)
        hour = goal.remind_at.hour
        minute = goal.remind_at.minute
        job_id = self.scheduler.add_job(self.send_email, 'cron', hour=hour, minute=minute, args=[self, goal]).id
        self.job_dict[user_id] = job_id
        print('registered job for '+user.username)

    @classmethod
    def send_mail_now(self, user_id):
        '''【デバッグ用】指定したユーザー宛に直ちにリマインドメールを送信する'''
        user = CustomUser.objects.get(pk=user_id)
        goal = Goals.objects.get(user=user, is_completed=False)
        self.send_email(self, goal)