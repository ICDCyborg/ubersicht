from django.contrib import admin
from .models import Goals, Todos, Records

# Register your models here.

class GoalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'is_completed')
    list_display_links = ('id', 'subject')

class TodosAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'state')
    list_display_links = ('id', 'title')

class RecordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'done_at', 'num')
    list_display_links = ('id', 'done_at', 'num')

admin.site.register(Goals, GoalsAdmin)
admin.site.register(Todos, TodosAdmin)
admin.site.register(Records, RecordsAdmin)