# Generated by Django 4.2.4 on 2023-09-05 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goals',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='records',
            old_name='todo_id',
            new_name='todo',
        ),
        migrations.RenameField(
            model_name='todos',
            old_name='goal_id',
            new_name='goal',
        ),
    ]
