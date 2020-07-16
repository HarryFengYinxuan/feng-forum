from datetime import datetime
import pytz

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from feng_forum_main.models import Topic, ForumThread
from feng_forum_user.models import ForumAccount

from .view_helper import ViewInstantiationTestCase, ViewBaseTestCase, \
                         OwnerOr404BaseTestCase, ForumThreadViewBaseTestCase

User = get_user_model()


class TopicListViewTestCase(ViewBaseTestCase, TestCase):
    view_name = 'topic-list'
    paginate_by = 7
    template = 'feng_forum_main/topic_list.html'
    paginate_key = 'page_obj'

    @classmethod
    def setUpTestData(cls,):
        for i in range(cls.paginate_by+1):
            Topic.objects.create(title=f'title{i}').save()

    def get_url_loc(self,):
        return '/main/topics/'


class ForumThreadDetailViewOO4TestCase(OwnerOr404BaseTestCase, TestCase):
    view_name = 'forumthread-detail'

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['pk'] = str(self.thread1.id)
        return kwargs

    
class ForumThreadDetailAccessTestCase(ForumThreadViewBaseTestCase, TestCase):
    view_name = 'forumthread-detail'
    paginate_by = 17
    template = 'feng_forum_main/forumthread_detail.html'
    paginate_key = 'replies_page'

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['pk'] = str(self.thread1.id)
        return kwargs

    def get_url_loc(self,):
        return f'/main/topics/{self.topic1.id}/forumthreads/{self.thread1.id}/'

    def test_pagination(self):
        if self.paginate_by >= 0:
            self.client.logout()
            if self.login_required:
                self.client.login(username='user1', password='pass1')
            response = self.client.get(reverse(
                self.view_name, 
                kwargs={
                    'topic_pk': str(self.topic1.id),
                    'pk': str(self.thread4.id),
                }))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                            self.paginate_by)

    def test_pagination_rest(self):
        if self.paginate_by >= 0:
            self.client.logout()
            if self.login_required:
                self.client.login(username='user1', password='pass1')
            response = self.client.get(
                reverse(self.view_name, kwargs={
                    'topic_pk': str(self.topic1.id),
                    'pk': str(self.thread4.id),
                }),
                {'page':'2'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                             1)

    
class TopicDetailViewAccessTestCase(ForumThreadViewBaseTestCase, TestCase):
    view_name = 'topic-detail'
    paginate_by = 7
    template = 'feng_forum_main/topic_detail.html'
    paginate_key = 'forumthread_page'

    @classmethod
    def setUpTestData(cls,):
        cls.user1 = User.objects.create_user(username='user1', 
                                             password='pass1')
        cls.user1.save()
        cls.user2 = User.objects.create_user(username='user2', 
                                             password='pass2')
        cls.user2.save()

        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        for i in range(cls.paginate_by+1):
            ForumThread.objects.create(
                title=f'title{i}',
                content=f'content{i}',
                user=cls.user1,
                topic=cls.topic1,
                new=True,
                reply_to=None,
                priviledged=False,
                top_level=None,
            ).save()

        content_type = ContentType.objects.get_for_model(ForumThread)
        for i in range(1):
            obj = ForumThread.objects.create(
                title=f'prvldg title{i}',
                content=f'priviledge content{i}',
                user=cls.user1,
                topic=cls.topic1,
                new=True,
                reply_to=None,
                priviledged=True,
                top_level=None,
            )
            obj.save()
            permission = Permission.objects.create(
                codename=obj.view_perm_codename_short(),
                name=obj.view_perm_name(),
                content_type=content_type,
            )
            cls.user1.user_permissions.add(permission)

    def get_url_loc(self,):
        return f'/main/topics/{self.topic1.id}/'

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['pk'] = str(self.topic1.id)
        return kwargs

    def test_pagination_rest(self):  # 特殊key覆盖
        if self.paginate_by >= 0:
            # 未登录不能看到高访问级别
            self.client.logout()
            response = self.client.get(
                reverse(self.view_name, kwargs=self.get_kwargs()),
                {'forumthread_page_num':'2'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                             1)

            # 无权限用户不能看到高访问级别
            self.client.logout()
            self.client.login(username='user2', password='pass2')
            response = self.client.get(
                reverse(self.view_name, kwargs=self.get_kwargs()),
                {'forumthread_page_num':'2'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                             1)

            # 有权限用户能看到高访问级别
            self.client.logout()
            self.client.login(username='user1', password='pass1')
            response = self.client.get(
                reverse(self.view_name, kwargs=self.get_kwargs()),
                {'forumthread_page_num':'2'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                             2)


class ForumThreadCreateViewTestCase(ForumThreadViewBaseTestCase, TestCase):
    view_name = 'forumthread-create'
    paginate_by = -1
    template = 'feng_forum_main/forumthread_form.html'
    paginate_key = ''
    login_required = True
    owned = False

    def get_url_loc(self,):
        return f'/main/topics/{self.topic1.id}/forumthreads/create/'

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        return kwargs


class ForumThreadUpdateViewOO4TestCase(OwnerOr404BaseTestCase, TestCase):
    view_name = 'forumthread-update'
    read_only = False

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['pk'] = str(self.thread1.id)
        return kwargs

    def get_post_data(self,):
        return {'title': '0123456789abcde',
                'content': 'content1',

                'new':'on',
                'topic': str(self.topic1.id),
                'user': str(self.user1.id),
                'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                # 'reply_to': None,
                # 'top_level': None,
                'deleted': True,

                # 'priviledged': False,
                'can_view': '',}

    
class ForumThreadUpdateAccessTestCase(ForumThreadViewBaseTestCase, TestCase):
    view_name = 'forumthread-update'
    paginate_by = -1
    template = 'feng_forum_main/forumthread_form.html'
    login_required = True

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['pk'] = str(self.thread1.id)
        return kwargs

    def get_url_loc(self,):
        return f'/main/topics/{self.topic1.id}/forumthreads/update/{self.thread1.id}/'

    def test_priviledged(self,):
        self.client.login(username='user2', password='pass2')
        response = self.client.get(reverse(self.view_name, kwargs={
            'topic_pk': str(self.topic1.id),
            'pk': str(self.thread3.id),
        }))
        self.assertEqual(response.status_code, 404)


class ForumThreadReplyCreateViewTestCase(OwnerOr404BaseTestCase, TestCase):
    view_name = 'forumthread-reply-create'
    read_only = False

    def test_owner_or_404_success(self,):
        pass  # 永远失败

    def test_owner_or_404_fail(self,):
        view_name = self.get_view_name()
        kwargs = self.get_kwargs()

        # 未登录get
        self.client.logout()
        response = self.client.get(reverse(view_name, kwargs=kwargs))
        if self.read_only:  # detail直接404
            self.assertEqual(response.status_code, 404)
        else:  # update需要登录
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/login/'))
        # 非发送用户登录get
        self.client.login(username='user2', password='pass2')
        response = self.client.get(reverse(view_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 404)
        # 本发送用户登录get，不允许回复自己已被删除的贴子。
        self.client.login(username='user1', password='pass1')
        response = self.client.get(reverse(view_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 404)

        if not self.read_only:  # post
            # 未登录post
            self.client.logout()
            response = self.client.post(reverse(view_name, kwargs=kwargs), 
                                        self.get_post_data())
            # post需要登录
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/login/'))
            # 非发送用户登录post
            self.client.login(username='user2', password='pass2')
            response = self.client.post(reverse(view_name, kwargs=kwargs), 
                                        self.get_post_data())
            self.assertEqual(response.status_code, 404)
            # 本发送用户登录post
            self.client.login(username='user1', password='pass1')
            response = self.client.post(reverse(view_name, kwargs=kwargs), 
                                        self.get_post_data())
            self.assertEqual(response.status_code, 404)

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['reply_pk'] = str(self.thread1.id)
        # kwargs['pk'] = str(self.thread1.id)
        return kwargs

    def get_post_data(self,):
        return {'title': '0123456789abcde',
                'content': 'content1@user3 @user2',

                # 'new':'on',
                'topic': str(self.topic1.id),
                'user': str(self.user1),
                'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reply_to': str(self.thread1.id),
                # 'top_level': None,
                'deleted': True,

                # 'priviledged': False,
                'can_view': '',}


class ForumThreadReplyUpdateViewTestCase(OwnerOr404BaseTestCase, TestCase):
    view_name = 'forumthread-reply-update'
    read_only = False

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        kwargs['reply_pk'] = str(self.thread1.id)
        kwargs['pk'] = str(self.thread2.id)
        return kwargs

    def get_post_data(self,):
        return {#'title': '',
                'content': 'content1',

                # 'new':'on',
                'topic': str(self.topic1.id),
                'user': str(self.user1.id),
                'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reply_to': str(self.thread1.id),
                # 'top_level': None,
                'deleted': True,

                # 'priviledged': False,
                'can_view': '',}


class ForumThreadInstantiationTestCase(ViewInstantiationTestCase, TestCase):
    view_name = 'forumthread-create'

    @classmethod
    def setUpTestData(cls,):
        super().setUpTestData()

        cls.user2 = User.objects.create_user(username='user2', 
                                             password='pass2')
        cls.user2.save()
        cls.user3 = User.objects.create_user(username='user3', 
                                             password='pass3')
        cls.user3.save()

        cls.account1 = ForumAccount.objects.create(user=cls.user1)
        cls.account1.save()
        cls.account2 = ForumAccount.objects.create(user=cls.user2)
        cls.account2.save()
        cls.account3 = ForumAccount.objects.create(user=cls.user3)
        cls.account3.save()

        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        cls.now = timezone.now().replace(microsecond=0)

    def get_kwargs(self,):
        kwargs = super().get_kwargs()
        kwargs['topic_pk'] = str(self.topic1.id)
        return kwargs

    def get_post_data(self,):
        return {'title': '0123456789abcde',
                'content': 'content1@user3 @user2',

                'new':'on',
                'topic': str(self.topic1.id),
                'user': str(self.user1.id),
                'post_datetime': self.now.strftime('%Y-%m-%d %H:%M:%S'),
                # 'reply_to': None,
                # 'top_level': None,
                'deleted': False,

                # 'priviledged': False,
                'can_view': '',}

    def check_created(self,):
        obj = ForumThread.objects.get(title='0123456789abcde')
        self.assertEqual(obj.title, '0123456789abcde')
        self.assertEqual(obj.content, 'content1@user3 @user2')
        self.assertEqual(obj.new, True)
        self.assertEqual(obj.post_datetime, self.now)
        self.assertEqual(len(obj.referenced.all()), 2)
        self.assertEqual(obj.user, self.user1)
        self.assertEqual(obj.reply_to, None)
        self.assertEqual(obj.top_level, None)
        self.assertEqual(obj.deleted, False)
        self.assertEqual(obj.priviledged, False)

