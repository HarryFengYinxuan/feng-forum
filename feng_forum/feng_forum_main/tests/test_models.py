from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from feng_forum_main.models import Topic, ForumThread, MicroForumThread

User = get_user_model()


class TopicTestCase(TestCase):

    @classmethod
    def setUpTestData(cls,):
        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        cls.test_user1 = User.objects.create_user(
            username='user1', 
            password='1X<ISRUkw+tuK')
        cls.test_user1.save()

        ForumThread.objects.create(
            title='forum thread 1',
            content='content 1',
            user=cls.test_user1,
            topic=cls.topic1,
        ).save()

        MicroForumThread.objects.create(
            content='micro content 1',
            user=cls.test_user1,
            topic=cls.topic1,
        ).save()

    def test_object_name(self,):
        self.assertEqual(str(self.topic1), self.topic1.title)

    def test_url(self,):
        self.assertEqual(self.topic1.get_absolute_url(), 
                          reverse('topic-detail', args=[str(self.topic1.id)]))

    def test_get_forumthreads(self,):
        self.assertEqual(list(self.topic1.get_forumthreads()),
                          list(self.topic1.forumthread_set.filter(new=True)\
                               .order_by('-post_datetime')))

    def test_get_microforumthreads(self,):
        self.assertEqual(list(self.topic1.get_microforumthreads()),
                          list(self.topic1.microforumthread_set\
                               .filter(new=True)\
                               .order_by('-post_datetime')))


class ForumThreadTestCase(TestCase):

    @classmethod
    def setUpTestData(cls,):
        cls.topic1 = Topic.objects.create(title='topic1')
        cls.topic1.save()

        cls.test_user1 = User.objects.create_user(
            username='user1', 
            password='1X<ISRUkw+tuK')
        cls.test_user1.save()

        cls.thread1 = ForumThread.objects.create(
            title='forum thread 1',
            content='content 1',
            user=cls.test_user1,
            topic=cls.topic1,
            new=True,
        )
        cls.thread1.save()

        cls.thread2 = ForumThread.objects.create(
            title='forum thread 2',
            content='content 2',
            user=cls.test_user1,
            topic=cls.topic1,
            new=False,
            reply_to=cls.thread1,
            top_level=cls.thread1,
        )
        cls.thread2.save()

        cls.thread3 = ForumThread.objects.create(
            title='forum thread 3',
            content='content 3',
            user=cls.test_user1,
            topic=cls.topic1,
            reply_to=cls.thread2,
            top_level=cls.thread1,
        )
        cls.thread3.save()

    def test_object_name(self,):
        self.assertEqual(str(self.thread1), self.thread1.title)
        self.assertEqual(str(self.thread2), f'回复{self.thread2.get_top()}')
        self.assertEqual(str(self.thread3), f'回复{self.thread3.get_top()}')

    def test_url(self,):
        self.assertEqual(self.thread1.get_absolute_url(),
                          reverse('forumthread-detail', args=[
                              str(self.thread1.topic.id), 
                              str(self.thread1.id)]))
        self.assertEqual(self.thread2.get_absolute_url(),
                          reverse('forumthread-detail', args=[
                              str(self.thread1.topic.id), 
                              str(self.thread1.id)]))
        self.assertEqual(self.thread3.get_absolute_url(),
                          reverse('forumthread-detail', args=[
                              str(self.thread1.topic.id), 
                              str(self.thread1.id)]))

    def test_get_top(self,):
        self.assertEqual(self.thread1.get_top(), self.thread1)
        self.assertEqual(self.thread2.get_top(), self.thread1)
        self.assertEqual(self.thread3.get_top(), self.thread1)

    def test_get_replies(self,):
        self.assertEqual(list(self.thread1.get_replies()),
                          list(self.thread1.forumthread_toplevel.all()\
                            .order_by('post_datetime')))
        self.assertRaises(AssertionError, self.thread2.get_replies)
        self.assertRaises(AssertionError, self.thread3.get_replies)

    def test_view_perm_codename_short(self,):
        # 只有1楼才需要高访问级别
        self.assertEqual(self.thread1.view_perm_codename_short(),
                          f'forumthread_{self.thread1.id}_can_view')

    def test_view_perm_codename(self,):
        # 只有1楼才需要高访问级别
        self.assertEqual(self.thread1.view_perm_codename(),
                          f'feng_forum_main.forumthread_'\
                          f'{self.thread1.id}_can_view')

    def test_view_perm_name(self,):
        # 只有1楼才需要高访问级别
        self.assertEqual(self.thread1.view_perm_name(),
                          ' '.join(self.thread1.view_perm_codename_short()\
                              .split('_')))
