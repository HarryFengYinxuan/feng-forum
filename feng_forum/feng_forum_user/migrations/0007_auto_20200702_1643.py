# Generated by Django 3.0.2 on 2020-07-02 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0006_auto_20200701_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='icon',
        ),
        migrations.CreateModel(
            name='ForumAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('女性', '女性'), ('男性', '男性'), ('无性别', '无性别'), ('双性别', '双性别'), ('变性', '变性'), ('随性', '随性'), ('其他', '其他'), ('不便透露', '不便透露')], default='不便透露', max_length=8, verbose_name='账户自我认同的性别')),
                ('show_name', models.BooleanField(default=False, verbose_name='显示姓名')),
                ('show_email', models.BooleanField(default=False, verbose_name='显示邮箱')),
                ('show_gender', models.BooleanField(default=False, verbose_name='显示性别')),
                ('show_last_login', models.BooleanField(default=False, verbose_name='显示上次登录时间')),
                ('show_date_joined', models.BooleanField(default=False, verbose_name='显示注册时间')),
                ('following', models.ManyToManyField(help_text='用户关注的人', to='feng_forum_user.ForumAccount')),
                ('user', models.OneToOneField(help_text='账户的用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
    ]