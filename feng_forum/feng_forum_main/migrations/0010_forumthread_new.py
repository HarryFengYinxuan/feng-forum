# Generated by Django 3.0.2 on 2020-07-03 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_main', '0009_auto_20200703_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumthread',
            name='new',
            field=models.BooleanField(default=False, verbose_name='新建帖子'),
        ),
    ]
