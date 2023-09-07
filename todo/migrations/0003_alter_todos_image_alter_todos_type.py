# Generated by Django 4.2.4 on 2023-09-07 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_rename_user_id_goals_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todos',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='todo/images/', verbose_name='画像'),
        ),
        migrations.AlterField(
            model_name='todos',
            name='type',
            field=models.CharField(choices=[('task', 'なし（タスク）'), ('training', '回（トレーニング）'), ('exam', '点（テスト）'), ('reading', 'ページ（読書）')], default='task', max_length=20, verbose_name='タイプ'),
        ),
    ]
