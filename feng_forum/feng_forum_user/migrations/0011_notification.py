# Generated by Django 3.0.2 on 2020-07-05 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0010_auto_20200702_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=15, verbose_name='信息内容')),
                ('link', models.URLField(verbose_name='信息链接')),
                ('read', models.BooleanField(default=False, verbose_name='看过')),
                ('account', models.ForeignKey(help_text='将信息送去的账户', null=True, on_delete=django.db.models.deletion.CASCADE, to='feng_forum_user.ForumAccount')),
            ],
            options={
                'verbose_name': '提示信息',
                'verbose_name_plural': '提示信息',
                'ordering': ['account'],
            },
        ),
    ]
