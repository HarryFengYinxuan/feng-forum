'''一些view测试的base class'''


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from feng_forum_main.models import Topic, ForumThread
from feng_forum_user.models import ForumAccount

User = get_user_model()


class OwnerOr404BaseTestCase:
    '''
    初始化一些数据然后创建新的case来测试在detail view是不是只有发贴子的用户可以看到贴子。
    简称OO4。
    '''

    # 把这个改成对应的值作为reverse的参数
    view_name = None
    read_only = True  # detail view
    
    @classmethod
    def setUpTestData(cls,):
        # 创建多个用户来测试@
        cls.user1 = User.objects.create_user(username='user1', 
                                             password='pass1')
        cls.user1.save()
        cls.account1 = ForumAccount.objects.create(user=cls.user1)
        cls.account1.save()
        cls.user2 = User.objects.create_user(username='user2', 
                                             password='pass2')
        cls.user2.save()
        cls.account2 = ForumAccount.objects.create(user=cls.user2)
        cls.account2.save()
        cls.user3 = User.objects.create_user(username='user3', 
                                             password='pass3')
        cls.user3.save()
        cls.account3 = ForumAccount.objects.create(user=cls.user3)
        cls.account3.save()

        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        cls.thread1 = ForumThread.objects.create(
            title='thread1',
            content='content1',
            user=cls.user1,
            topic=cls.topic1,
            deleted=True,
            new=True,
        )
        cls.thread1.save()

        cls.thread2 = ForumThread.objects.create(
            title='thread2',
            content='content2',
            user=cls.user1,
            topic=cls.topic1,
            deleted=True,
            new=False,
            reply_to=cls.thread1,
        )
        cls.thread2.save()

    def test_owner_or_404_success(self,):
        view_name = self.get_view_name()
        kwargs = self.get_kwargs()

        self.client.login(username='user1', password='pass1')
        response = self.client.get(reverse(view_name, kwargs=kwargs))
        self.assertEqual(response.status_code, 200)

        if not self.read_only:
            response = self.client.post(reverse(view_name, kwargs=kwargs), 
                                        self.get_post_data())
            self.assertEqual(response.status_code, 302)  # 成功跳转
            self.assertFalse(response.url.startswith('/accounts/login/'))

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

    def get_view_name(self,):
        assert isinstance(self.view_name, str)

        return self.view_name

    def get_kwargs(self,):
        return {}

    def get_post_data(self,):
        return {'title': '0123456789abcde',
                'content': 'content1',

                # 'new':'on',
                'topic': str(self.topic1.id),
                'user': str(self.user1),
                'post_datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reply_to': None,
                # 'top_level': None,
                # 'deleted': False,

                # 'priviledged': False,
                'can_view': '',}


class ViewBaseTestCase:
    '''
    测url_location, url_by_name, template, pagination。
    '''

    view_name = ''
    paginate_by = 0  # 如果值小于0就跳过pagination测试
    template = ''
    paginate_key = ''
    login_required = False

    @classmethod
    def setUpTestData(cls,):
        pass

    def test_url_location(self,):
        self.client.logout()
        if self.login_required:
            self.client.login(username='user1', password='pass1')
        response = self.client.get(self.get_url_loc())
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self,):
        self.client.logout()
        if self.login_required:
            self.client.login(username='user1', password='pass1')
        response = self.client.get(reverse(self.view_name, 
                                           kwargs=self.get_kwargs()))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        self.client.logout()
        if self.login_required:
            self.client.login(username='user1', password='pass1')
        response = self.client.get(reverse(self.view_name, 
                                           kwargs=self.get_kwargs()))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_pagination(self):
        if self.paginate_by >= 0:
            self.client.logout()
            if self.login_required:
                self.client.login(username='user1', password='pass1')
            response = self.client.get(reverse(
                self.view_name, 
                kwargs=self.get_kwargs()))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                            self.paginate_by)

    def test_pagination_rest(self):
        if self.paginate_by >= 0:
            self.client.logout()
            if self.login_required:
                self.client.login(username='user1', password='pass1')
            response = self.client.get(
                reverse(self.view_name, kwargs=self.get_kwargs()),
                {'page':'2'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[self.paginate_key]),
                             1)

    def test_login_redirect(self,):
        if self.login_required:
            self.client.logout()
            response = self.client.get(reverse(self.view_name, 
                                               kwargs=self.get_kwargs()))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/login/'))

    def get_kwargs(self,):
        return {}

    def get_url_loc(self,):
        return ''


class ForumThreadViewBaseTestCase(ViewBaseTestCase):
    '''
    测url_location, url_by_name, template, pagination。
    '''
    owned = True  # 贴子是不是属于一个用户。创建不属于另一个用户。

    @classmethod
    def setUpTestData(cls,):
        # 创建多个用户来测试@

        # 用户1有权限，创建了贴子
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

        # 正常1楼
        cls.thread1 = ForumThread.objects.create(
            title='thread1',
            content='content1',
            user=cls.user1,
            topic=cls.topic1,
            deleted=False,
            new=True,
        )
        cls.thread1.save()

        # 正常回复贴
        cls.thread2 = ForumThread.objects.create(
            title='thread2',
            content='content2',
            user=cls.user1,
            topic=cls.topic1,
            deleted=False,
            new=False,
            reply_to=cls.thread1,
        )
        cls.thread2.save()

        # 高访问权限1楼
        cls.thread3 = ForumThread.objects.create(
            title='thread3',
            content='content3',
            user=cls.user1,
            topic=cls.topic1,
            deleted=False,
            new=True,
            reply_to=None,
            priviledged=True,
        )
        cls.thread3.save()

        # 测pagination1楼
        cls.thread4 = ForumThread.objects.create(
            title='thread4',
            content='content4',
            user=cls.user1,
            topic=cls.topic1,
            deleted=False,
            new=True,
            reply_to=None,
            priviledged=False,
        )
        cls.thread4.save()

        for i in range(cls.paginate_by+1):
            ForumThread.objects.create(
                title=f'reply{i}',
                content=f'content of reply{i}',
                user=cls.user2,
                topic=cls.topic1,
                new=False,
                reply_to=cls.thread4,
                priviledged=False,
                top_level=cls.thread4,
            ).save()

        # 给user1加权限
        content_type = ContentType.objects.get_for_model(ForumThread)
        obj = cls.thread3
        permission = Permission.objects.create(
            codename=obj.view_perm_codename_short(),
            name=obj.view_perm_name(),
            content_type=content_type,
        )
        cls.user1.user_permissions.add(permission)

    def test_bad_user_edit(self,):
        if self.owned and self.login_required:
            self.client.login(username='user2', password='pass2')
            response = self.client.get(reverse(self.view_name, 
                                            kwargs=self.get_kwargs()))
            self.assertEqual(response.status_code, 401)


class UserModifyTestCase:
    view_name = ''

    @classmethod
    def setUpTestData(cls,):
        cls.user1 = User.objects.create_user(username='user1', 
                                             password='pass1')
        cls.user1.save()

    def test_success(self,):
        view_name = self.view_name
        kwargs = self.get_kwargs()

        self.client.login(username='user1', password='pass1')
        response = self.client.post(reverse(view_name, kwargs=kwargs), 
                                    self.get_post_data())
        self.assertEqual(response.status_code, 302)  # 成功跳转
        self.assertFalse(response.url.startswith('/accounts/login/'))
        self.check_created()

    def get_post_data(self,):
        return {}

    def get_kwargs(self,):
        return {}

    def check_created(self,):
        return None