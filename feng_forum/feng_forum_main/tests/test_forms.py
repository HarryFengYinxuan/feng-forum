from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from feng_forum_main.forms import ForumThreadCreateForm
from feng_forum_main.models import Topic, ForumThread

User = get_user_model()


class ForumThreadCreateFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls,):
        # 创建多个用户来测试@
        cls.user1 = User.objects.create_user(username='user1', 
                                             password='pass1')
        cls.user1.save()
        cls.user2 = User.objects.create_user(username='user2', 
                                             password='pass2')
        cls.user2.save()
        cls.user3 = User.objects.create_user(username='user3', 
                                             password='pass3')
        cls.user3.save()

        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        cls.thread1 = ForumThread.objects.create(
            title='thread1',
            content='content1',
            user=cls.user1,
            topic=cls.topic1,
            new=True,
        )
        cls.thread1.save()

        # 此贴已被删除。
        cls.thread2 = ForumThread.objects.create(
            title='thread2',
            content='content2',
            user=cls.user1,
            topic=cls.topic1,
            new=True,
            deleted=True,
        )
        cls.thread2.save()

    def test_valid(self,):
        form = ForumThreadCreateForm({
            'title': '0123456789abcde',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': True,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': None,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertTrue(form.is_valid())

        form = ForumThreadCreateForm({
            'title': '',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': False,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': self.thread1,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        temp = form.is_valid()
        self.assertTrue(temp)

    def test_invalid(self,):
        # title too long
        form = ForumThreadCreateForm({
            'title': '0123456789abcdef',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': True,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': None,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())

        # datetime格式错误
        form = ForumThreadCreateForm({
            'title': '0123456789abcde',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': True,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S etc'),
            'reply_to': None,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())

        # 一楼不可以回复
        form = ForumThreadCreateForm({
            'title': '0123456789abcde',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': True,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': self.thread1,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())

        # 一楼以外必须是回复
        form = ForumThreadCreateForm({
            'title': '0123456789abcde',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': False,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': None,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())

        # # 回复帖不存在。
        # form = ForumThreadCreateForm({
        #     'title': '0123456789abcde',
        #     'content': 'content1@user3 @user2',

        #     'topic': self.topic1.id,
        #     'user': self.user1,
        #     'new': True,
        #     'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        #     'reply_to': self.thread2,
        #     'top_level': None,
        #     'deleted': False,

        #     'priviledged': False,
        #     'can_view': '',
        # })
        # self.assertFalse(form.is_valid())

        # 回复没有高访问权限。
        form = ForumThreadCreateForm({
            'title': '0123456789abcde',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': False,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': self.thread1,
            'top_level': None,
            'deleted': False,

            'priviledged': True,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())

        # 回复没有标题。
        form = ForumThreadCreateForm({
            'title': 'bad title',
            'content': 'content1@user3 @user2',

            'topic': self.topic1.id,
            'user': self.user1,
            'new': False,
            'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reply_to': self.thread1,
            'top_level': None,
            'deleted': False,

            'priviledged': False,
            'can_view': '',
        })
        self.assertFalse(form.is_valid())