from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from feng_forum_user.models import User, ForumAccount, Notification
from feng_forum_upload.models import UploadedMedia

class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls,):
        # 用户1有一个头像
        cls.test_user1 = User.objects.create_user(
            username='user1',
            password='1X<ISRUkw+tuK',
        )
        cls.test_user1.save()

        cls.uploaded1 = UploadedMedia.objects.create(
            name='uploaded1',
            user=cls.test_user1,
            is_icon=True,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded1.png', 
                content=open('feng_forum_user/tests/test_uploaded1.png', 
                             'rb').read(), 
                # content_type='image/jpeg',
                )
        )
        cls.uploaded1.save()

        UploadedMedia.objects.create(
            name='uploaded2',
            user=cls.test_user1,
            is_icon=False,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded2.jpg', 
                content=open('feng_forum_user/tests/test_uploaded2.jpg', 
                             'rb').read(), 
                content_type='image/jpeg')
        ).save()

        # 用户2有0个头像
        cls.test_user2 = User.objects.create_user(
            username='user2',
            password='2HJ1vRV0Z&3iD',
        )
        cls.test_user2.save()

        UploadedMedia.objects.create(
            name='uploaded3',
            user=cls.test_user2,
            is_icon=False,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded1.png', 
                content=open('feng_forum_user/tests/test_uploaded1.png', 
                             'rb').read(), 
                # content_type='image/jpeg',
                )
        ).save()

        UploadedMedia.objects.create(
            name='uploaded2',
            user=cls.test_user2,
            is_icon=False,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded2.jpg', 
                content=open('feng_forum_user/tests/test_uploaded2.jpg', 
                             'rb').read(), 
                content_type='image/jpeg')
        ).save()

        # 用户3有2个头像
        cls.test_user3 = User.objects.create_user(
            username='user3',
            password='2HJ1vRV0Z&3iD',
        )
        cls.test_user3.save()

        UploadedMedia.objects.create(
            name='uploaded3',
            user=cls.test_user3,
            is_icon=True,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded1.png', 
                content=open('feng_forum_user/tests/test_uploaded1.png', 
                             'rb').read(), 
                # content_type='image/jpeg',
                )
        ).save()

        UploadedMedia.objects.create(
            name='uploaded2',
            user=cls.test_user3,
            is_icon=True,
            uploaded_img=SimpleUploadedFile(
                name='test_uploaded2.jpg', 
                content=open('feng_forum_user/tests/test_uploaded2.jpg', 
                             'rb').read(), 
                content_type='image/jpeg')
        ).save()

    def test_object_name(self,):
        self.assertEqual(str(self.test_user1), 'user1')
        self.assertEqual(str(self.test_user2), 'user2')
        self.assertEqual(str(self.test_user3), 'user3')

    def test_get_icon_url(self,):
        self.assertEqual(self.test_user1.get_icon_url(),
                          self.uploaded1.uploaded_img.url)
        self.assertEqual(self.test_user2.get_icon_url(), None)  # 无头像
        self.assertEqual(self.test_user2.get_icon_url(), None)  # 多头像


class ForumAccountTestCase(TestCase):

    @classmethod 
    def setUpTestData(cls,):
        # 账户1有一条未读，共有2条消息
        cls.test_user1 = User.objects.create_user(
            username='user1',
            password='1X<ISRUkw+tuK',
        )
        cls.test_user1.save()

        cls.account1 = ForumAccount.objects.create(user=cls.test_user1)

        Notification.objects.create(
            forumaccount=cls.account1,
            message='msg1',
        )

        Notification.objects.create(
            forumaccount=cls.account1,
            message='msg2',
            read=True,
        )
        
        # 账户2有一条未读，共有3条消息
        cls.test_user2 = User.objects.create_user(
            username='user2',
            password='1X<ISRUkw+tuK',
        )
        cls.test_user2.save()

        cls.account2 = ForumAccount.objects.create(user=cls.test_user2)

        Notification.objects.create(
            forumaccount=cls.account2,
            message='msg3',
        )

        Notification.objects.create(
            forumaccount=cls.account2,
            message='msg4',
        )

        Notification.objects.create(
            forumaccount=cls.account2,
            message='msg5',
            read=True,
        )

    def test_object_name(self,):
        self.assertEqual(str(self.account1), f'{self.test_user1} 的账户')
        self.assertEqual(str(self.account2), f'{self.test_user2} 的账户')

    def test_get_messages(self,):
        self.assertEqual(list(self.account1.get_messages()), 
                          list(self.account1.notification_set.all()))
        self.assertEqual(list(self.account2.get_messages()), 
                          list(self.account2.notification_set.all()))

    def test_get_unread_message_count(self,):
        self.assertEqual(self.account1.get_unread_message_count(),
                          self.account1.get_messages()\
                              .filter(read=False)\
                              .count())
        self.assertEqual(self.account2.get_unread_message_count(),
                          self.account2.get_messages()\
                              .filter(read=False)\
                              .count())


class NotificationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls,):
        cls.test_user1 = User.objects.create_user(
            username='user1',
            password='1X<ISRUkw+tuK',
        )
        cls.test_user1.save()

        cls.account1 = ForumAccount.objects.create(user=cls.test_user1)
        cls.account1.save()

        cls.msg1 = Notification.objects.create(
            forumaccount=cls.account1,
            message='msg1',
        )
        cls.msg1.save()
        
        cls.test_user2 = User.objects.create_user(
            username='user2',
            password='1X<ISRUkw+tuK',
        )
        cls.test_user2.save()

        cls.account2 = ForumAccount.objects.create(user=cls.test_user2)
        cls.account2.save()

        cls.msg2 = Notification.objects.create(
            forumaccount=cls.account2,
            message='msg2',
        )
        cls.msg2.save()

    def test_object_name(self,):
        self.assertEqual(str(self.msg1), 'msg1')
        self.assertEqual(str(self.msg2), 'msg2')

    def test_url(self,):
        self.assertEqual(self.msg1.get_absolute_url(), 
                          reverse('notification-list'))
        self.assertEqual(self.msg2.get_absolute_url(), 
                          reverse('notification-list'))
