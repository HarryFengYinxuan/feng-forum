# Generated by Django 3.0.2 on 2020-07-07 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0018_auto_20200707_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(blank=True, max_length=50, verbose_name='信息链接'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=100, verbose_name='信息内容'),
        ),
    ]
