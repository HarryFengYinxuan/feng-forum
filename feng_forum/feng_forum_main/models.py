import re

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import django.contrib.auth

import pytz


class Topic(models.Model):
    '''
    贴吧
    '''

    title = models.CharField('标题', max_length=15, default='未命名', 
                             null=True)


    class Meta:
        ordering = ['title']
        verbose_name = '贴吧'
        verbose_name_plural = verbose_name


    def __str__(self,):
        return self.title

    def get_absolute_url(self,):
        return reverse('topic-detail', args=[str(self.id)])

    def get_forumthreads(self,):
        return self.forumthread_set.filter(new=True).order_by('-post_datetime')

    def get_microforumthreads(self,):
        return self.microforumthread_set.filter(new=True)\
            .order_by('-post_datetime')

class BaseForumThread(models.Model):
    '''
    普通贴子的基本操作模型。
    '''

    new = models.BooleanField('新建', default=False)
    content = models.TextField('贴子的内容')
    post_datetime = models.DateTimeField('发贴时间', default=timezone.now)
    
    class Meta:
        abstract = True
        ordering = ['-post_datetime']

    def get_brief_content(self,):
        c = self.content
        if len(c) > 15:
            return c[:15] + '。。。'
        else: 
            return c


class ForumThread(BaseForumThread):
    '''
    一个贴子可以富文本编辑内容。
    '''

    title = models.CharField('标题', max_length=15, default='未命名', 
                             null=True)  # 只有一楼标题才不是空
    # content = None  # change this to ckeditor
    topic = models.ForeignKey(
        'Topic', 
        help_text='本帖所在的贴吧。',
        on_delete=models.CASCADE,
        null=True,
    )
    referenced = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='forumthread_referenced',
        help_text='@ 到的用户。',
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='forumthread_user',
        help_text='发送的用户。',
        on_delete=models.CASCADE,
        null=True,
    )
    reply_to = models.ForeignKey(
        'ForumThread', 
        help_text='作为什么贴子的回复。',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='forumthread_replyto',
    )  # 如果是空代表是新建贴子
    top_level = models.ForeignKey(
        'ForumThread',
        help_text='一楼',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='forumthread_toplevel',
    )  # 优化的特殊快捷链接

    # 如果已删除，暂定会显示贴子已删除而不是从数据库删除。
    deleted = models.BooleanField('已删除', default=False)
    priviledged = models.BooleanField('高访问级别', default=False)


    class Meta:
        verbose_name = '贴子'
        verbose_name_plural = verbose_name

    
    def __str__(self,):
        # return self.title
        if self.new:
            return self.title
        else:
            return f'回复{self.get_top()}'

    def get_absolute_url(self,):
        if self.new:
            return reverse('forumthread-detail', 
                           args=[str(self.topic.id), str(self.id)])
        else:
            return self.get_top().get_absolute_url()  

    def get_top(self,):
        # 找一楼
        if self.new: 
            return self
        else:
            return self.top_level

    def get_replies(self,):
        assert self.new  # 一楼调用才有意义
        ret = self.forumthread_toplevel.all().order_by('post_datetime')
        return ret

    def view_perm_codename_short(self,):
        return f'forumthread_{self.id}_can_view'

    def view_perm_codename(self,):
        return f'feng_forum_main.forumthread_{self.id}_can_view'

    def view_perm_name(self,):
        return ' '.join(self.view_perm_codename_short().split('_'))


class MicroForumThread(BaseForumThread):
    '''
    微贴：内容为简单文字，可以附加多媒体，也可以回复。
    '''

    
    topic = models.ForeignKey(
        'Topic', 
        help_text='本微帖所在的贴吧。',
        on_delete=models.CASCADE,
        null=True)
    uploaded_media = models.ManyToManyField(
        'feng_forum_upload.UploadedMedia',
        help_text='贴子内包括的多媒体。',
        blank=True,
    )
    referenced = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='microforumthread_referenced',
        help_text='@ 到的用户。',
        blank=True,
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='microforumthread_user',
        help_text='发送的用户。',
        on_delete=models.CASCADE,
        null=True,
    )
    reply_to = models.ForeignKey(
        'MicroForumThread', 
        help_text='作为什么微贴的回复。',
        blank=True,
        null=True,
        on_delete=models.CASCADE)  # 如果是空代表是新建贴子


    class Meta:
        verbose_name = '微贴'
        verbose_name_plural = verbose_name

    
    def __str__(self,):
        return self.get_brief_content()

    def get_absolute_url(self,):
        return reverse('microforumthread-detail', args=[str(self.id)])

    def get_replies(self,):
        return self.microforumthread_set.all()



def get_ref_user(content, check=False):
    '''
    从字符串中找到@开头的用户名，并且返回其用户（列表）。
    如果check并且有错误，返回错误用户名（字符串）。
    '''
    
    assert isinstance(content, str)
    User = django.contrib.auth.get_user_model()

    raw_matched = re.findall(r'@\w*\s|@\w*$', content)  # 寻找匹配
    usernames = [i.rstrip()[1:] for i in raw_matched]  # 生成用户名
    users = []
    for name in usernames:
        try:
            users.append(User.objects.get(username=name))
        except User.DoesNotExist:
            if check:  # 检查是不是每一个都正确
                return name
    return users