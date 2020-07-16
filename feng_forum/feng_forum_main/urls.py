from django.urls import path

from .views import TopicListView, TopicDetailView, TopicCreateView, \
                   TopicUpdateView, TopicDeleteView, \
                   ForumThreadDetailView, \
                   ForumThreadCreateView, ForumThreadUpdateView, \
                   ForumThreadReplyCreateView, ForumThreadReplyUpdateView, \
                   MicroForumThreadDetailView, MicroForumThreadCreateView

urlpatterns = [
    # 贴吧
    path('topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topics/create/', TopicCreateView.as_view(), name='topic-create'),
    path('topics/update/<int:pk>/', TopicUpdateView.as_view(), 
         name='topic-update'),
    path('topics/delete/<int:pk>/', TopicDeleteView.as_view(), 
         name='topic-delete'),
    # 贴子
    path('topics/<int:topic_pk>/forumthreads/<int:pk>/', 
         ForumThreadDetailView.as_view(), 
         name='forumthread-detail'),
    path('topics/<int:topic_pk>/forumthreads/create/', 
         ForumThreadCreateView.as_view(), 
         name='forumthread-create'),
    path('topics/<int:topic_pk>/forumthreads/update/<int:pk>/', 
         ForumThreadUpdateView.as_view(), 
         name='forumthread-update'),
    path('topics/<int:topic_pk>/forumthreads/<int:reply_pk>/reply/', 
         ForumThreadReplyCreateView.as_view(), 
         name='forumthread-reply-create'),
    path('topics/<int:topic_pk>/forumthreads/<int:reply_pk>/<int:pk>', 
         ForumThreadReplyUpdateView.as_view(), 
         name='forumthread-reply-update'),
    # 微贴
    path('microforumthreads/<int:pk>/', MicroForumThreadDetailView.as_view(), 
         name='microforumthread-detail'),
    path('microforumthreads/create/', MicroForumThreadCreateView.as_view(), 
         name='microforumthread-create'),
]