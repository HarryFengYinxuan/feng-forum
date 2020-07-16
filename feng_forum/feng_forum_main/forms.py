from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Topic, ForumThread, MicroForumThread, get_ref_user
from feng_forum_user.models import User, Notification


class TopicCreateForm(forms.ModelForm):


    class Meta:
        model = Topic
        fields = '__all__'


class ForumThreadCreateForm(forms.ModelForm):
    can_view = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self,):
        cleaned_data = super().clean()
        new = cleaned_data.get('new')
        title = cleaned_data.get('title')
        reply_to = cleaned_data.get('reply_to')
        priviledged = cleaned_data.get('priviledged')

        if new and reply_to:
            raise forms.ValidationError('一楼不可以回复其他帖子。')

        if not new and not reply_to:
            raise forms.ValidationError('一楼以外必须是回复。')

        if reply_to and priviledged:
            raise forms.ValidationError('回复没有高访问权限。')

        if title and reply_to:
            raise forms.ValidationError('回复没有标题。')

    def clean_can_view(self,):
        data = self.cleaned_data['can_view']
        ret = get_ref_user(data, check=True)
        if isinstance(ret, str):  # 表达填写错误
            raise forms.ValidationError(f'用户{ret}不存在。')

        return ret

    # def clean_title(self,):
    #     data = self.cleaned_data['title']
    #     if len(data) > 15:  # 表达填写错误
    #         raise forms.ValidationError(f'标题长度不能大于15，目前长度{len(data)}。')

    #     return data

    # def clean_reply_to(self,):
    #     data = self.cleaned_data['reply_to']

    #     if data and data.deleted:
    #         # 这里需要也改一下默认的报错，不然也没啥用。
    #         raise forms.ValidationError('回复帖不存在。')

    #     return data
    
    def send_notifications(self,):
        self.send_notifications_replies()
        self.send_notifications_references()

    def send_notifications_references(self,):
        for user in self.instance.referenced.all():
            message = Notification.objects.create(
                forumaccount=user.forumaccount,
                message=f'{user.username}在贴子'
                        f'{self.instance.title}中@了您。',
                link=self.instance.get_absolute_url(),
                read=False,
            )

    def send_notifications_replies(self,):
        if self.cleaned_data['new']:
            return
        reply_to_thread = self.cleaned_data['reply_to']
        user = self.cleaned_data['user']
        message = Notification.objects.create(
            forumaccount=reply_to_thread.user.forumaccount,
            message=f'{user.username}回复了您的贴子{reply_to_thread}。',
            link=reply_to_thread.get_absolute_url(),
            read=False,
        )

    def get_top(self,):
        ''' 也许save之后运行，找到一楼。'''
        assert self.instance
        if not self.instance.new:
            self.instance.top_level = self.instance.reply_to.get_top()

    def handle_perm(self,):
        '''为高访问级别贴子创建权限，并发给有权限的用户，自动包括创建者。'''
        content_type = ContentType.objects.get_for_model(ForumThread)
        obj = self.instance
        try:
            permission = Permission.objects.get(
                codename=obj.view_perm_codename_short())
        except Permission.DoesNotExist:
            permission = Permission.objects.create(
                codename=obj.view_perm_codename_short(),
                name=obj.view_perm_name(),
                content_type=content_type,
            )
        users = User.objects.filter(user_permissions=permission)
        # 撤销旧的权限
        for u in users:
            u.user_permissions.remove(permission)
        # 授权
        for user in self.cleaned_data['can_view']:
            user.user_permissions.add(permission)
        obj.user.user_permissions.add(permission)


    class Meta:
        model = ForumThread
        fields = '__all__'


class MicroForumThreadCreateForm(forms.ModelForm):


    class Meta:
        model = MicroForumThread
        fields = '__all__'

