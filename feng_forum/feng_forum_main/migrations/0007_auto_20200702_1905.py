# Generated by Django 3.0.2 on 2020-07-02 19:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_main', '0006_auto_20200702_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumthread',
            name='post_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发贴时间'),
        ),
        migrations.AlterField(
            model_name='microforumthread',
            name='post_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发贴时间'),
        ),
    ]
