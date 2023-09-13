from django.apps import AppConfig

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'
    initialized = False

    def ready(self):
        print(self.initialized)
        self.initialized=True
        print('todo ready')
        super().ready()
        from . import mail
        mail.MailScheduler.schedule_email_init()
        mail.MailScheduler.scheduler.start()