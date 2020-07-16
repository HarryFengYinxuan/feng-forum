from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned
from django.urls import reverse

from feng_forum import settings

from feng_forum_upload.models import UploadedMedia


def user_icon_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # 这是一个特殊的上传情况,直接和用户相关
    return 'user_{0}/{1}'.format(instance.id, filename)

class User(AbstractUser):
    '''
    有头像的中文用户模型。
    '''

    description = models.CharField('介绍', max_length=100, blank=True)
    name = models.CharField('姓名', max_length=100, blank=True)
    username = models.CharField('用户名', max_length=100, unique=True)
    email = models.EmailField('邮箱')

    # removing
    first_name = None
    last_name = None


    class Meta:
        ordering = ['username']
        verbose_name = "用户"
        verbose_name_plural = verbose_name



    def get_icon_url(self,):
        try:
            return self.uploadedmedia_user.get(is_icon=True).uploaded_img.url
        except (UploadedMedia.DoesNotExist, MultipleObjectsReturned):
            return None

    def __str__(self,):
        return self.username 

    def get_absolute_url(self,):
        return '/'


class ForumAccount(models.Model):
    '''
    和用户一对一的账户。可以关注别的账户、可以设置、可以有简单扩展。
    '''

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text='账户的用户')
    following = models.ManyToManyField(
        'ForumAccount',
        help_text='用户关注的人',
        blank=True)
    gender = models.CharField(
        '账户自我认同的性别',
        max_length=8,
        choices=[
            ('女性', '女性'),
            ('男性', '男性'),
            ('无性别', '无性别'),
            ('双性别', '双性别'),
            ('变性', '变性'),
            ('随性', '随性'),
            ('其他', '其他'),
            ('不便透露', '不便透露'),
        ],
        default='不便透露',
    )

    # show settings
    show_name = models.BooleanField('显示姓名', default=False)
    show_email = models.BooleanField('显示邮箱', default=False)
    show_gender = models.BooleanField('显示性别', default=False)
    show_last_login = models.BooleanField('显示上次登录时间', default=False)
    show_date_joined = models.BooleanField('显示注册时间', default=False)

    class Meta:
        ordering = ['user']
        verbose_name = '账户'
        verbose_name_plural = verbose_name

    
    def get_messages(self,):
        return self.notification_set.all()

    def get_unread_message_count(self,):
        return self.get_messages().filter(read=False).count()

    def __str__(self,):
        return f'{self.user} 的账户'

    def get_absolute_url(self,):
        return '/' 


class Notification(models.Model):
    '''
    账户的一条提示信息，例如贴子回复。
    '''

    forumaccount = models.ForeignKey('ForumAccount', 
                                     help_text="将信息送去的账户",
                                     on_delete=models.CASCADE,
                                     null=True)
    message = models.CharField('信息内容', max_length=100)
    link = models.CharField('信息链接', max_length=100, blank=True)
    read = models.BooleanField('已读', default=False)
    sent_datetime = models.DateTimeField('发送时间', default=timezone.now)


    class Meta:
        ordering = ['-sent_datetime']
        verbose_name = '提示信息'
        verbose_name_plural = verbose_name


    def __str__(self,):
        return self.message 

    def get_absolute_url(self,):
        return reverse('notification-list')

    