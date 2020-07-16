# Generated by Django 3.0.2 on 2020-07-01 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0003_auto_20200701_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='用户名'),
        ),
    ]