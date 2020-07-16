from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, \
                                      FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Topic, ForumThread, MicroForumThread, get_ref_user
# from feng_forum_user.models import User
from django.contrib.auth import get_user_model
from .forms import TopicCreateForm, ForumThreadCreateForm, \
                   MicroForumThreadCreateForm

User = get_user_model()

def owner_or_404(func):
    '''
    用在forumthread的view的post和get上。对于已删除的贴子来说，发送的用户以外
    不会看到这个网页。
    '''
    def wrapper(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:  # create
            # 创建的时候任何和创建有关的对象不能是已删除
            if self.required_deleted():
                return HttpResponse(status=404)
        if obj and obj.deleted and request.user.id != obj.user.id:  # update
            return HttpResponse(status=404)
        return func(self, request, *args, **kwargs)
    return wrapper

def owner_or_401(func):
    '''
    用在forumthread的formview上，如果登录的不是发帖用户，返回401访问限制。
    '''
    def wrapper(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj and request.user.id != obj.user.id: 
            return HttpResponse(status=401)
        return func(self, request, *args, **kwargs)
    return wrapper

def can_view_or_404(func):
    '''
    用在forumthread的formview上，没有权限的用户访问高访问级别贴子的时候有两种情况。
    1. detailview, formview访问
    2. 回复formview访问
    '''
    def wrapper(self, request, *args, **kwargs):
        if 'reply_pk' in self.kwargs or 'pk' in self.kwargs: 
            # 有reply pk自然要看obj权限。否则有pk也是更新要看权限。创建不看权限。
            if 'reply_pk' in self.kwargs:  # 回复formview访问
                obj = self.model.objects.get(id=self.kwargs['reply_pk'])
            else:  # detailview, formview访问
                obj = self.get_object()

            assert obj 
            if request.user.is_anonymous:
                user = None
            else:
                user = User.objects.get(id=request.user.id)
            user_no_perm = request.user.is_anonymous \
                        or not user.has_perm(obj.view_perm_codename())
            if obj.priviledged and user_no_perm:
                return HttpResponse(status=404)

        # 正常response
        return func(self, request, *args, **kwargs)
    return wrapper

def forumthread_post_view_check(func):
    # 先查404，再查401
    return can_view_or_404(owner_or_404(owner_or_401(func)))


# === 贴吧 ===

class TopicListView(ListView):
    model = Topic
    paginate_by = 7


class TopicDetailView(DetailView):
    model = Topic
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        forumthreads = context['topic'].get_forumthreads()
        # 检查用户访问权限
        if self.request.user.is_anonymous:
            forumthreads = forumthreads.filter(priviledged=False)
        else:
            user = User.objects.get(id=self.request.user.id)
            exclude_list = [entry.id \
                            for entry in forumthreads \
                            if not user.has_perm(entry.view_perm_codename()) \
                               and entry.priviledged]
            forumthreads = forumthreads.exclude(id__in=exclude_list)
        paginator = Paginator(forumthreads, self.paginate_by)

        page_number = self.request.GET.get('forumthread_page_num')
        forumthread_page = paginator.get_page(page_number)
        context['forumthread_page'] = forumthread_page
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicCreateForm


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicCreateForm


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy('topic-list')


# === 贴子 ===


class ForumThreadDetailView(DetailView):
    model = ForumThread
    paginate_by = 17

    @owner_or_404
    @can_view_or_404
    def get(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['forumthread'].get_replies(), self.paginate_by)

        page_number = self.request.GET.get('page')
        replies_page = paginator.get_page(page_number)
        context['replies_page'] = replies_page
        return context


class ForumThreadBaseView(LoginRequiredMixin, FormView):
    '''
    负责创建、更新和回复。
    '''

    template_name = 'feng_forum_main/forumthread_form.html'
    model = ForumThread
    form_class = ForumThreadCreateForm
    is_new = True  # 1楼
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime_now'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        context['topic'] = self.kwargs['topic_pk']
        context['is_new'] = self.is_new
        context['reply_to_val'] = '' \
                                  if self.is_new \
                                  else self.kwargs['reply_pk']
        return context

    def get_object(self,):
        # 不用mixin先写个简易的
        # 决定是创建还是更改，有pk是更改。
        if self.object:
            pass
        else:
            self.object = self.model.objects.get(id=self.kwargs['pk']) \
                          if 'pk' in self.kwargs \
                          else None
        return self.object 

    def get_initial(self,):
        obj = self.get_object()

        instance_initial = {'title': obj.title, 
                            'content': obj.content, 
                            'priviledged': obj.priviledged,
                            'deleted': obj.deleted} \
                           if obj \
                           else {'title': '未命名'}

        # 如果高访问级别找到有权限的用户
        if obj and obj.priviledged:
            perm = Permission.objects.get(
                codename=obj.view_perm_codename_short())
            users = User.objects.filter(Q(user_permissions=perm))
            instance_initial['can_view'] = ' '.join([f'@{u.username}' \
                                                     for u \
                                                     in users])
        return instance_initial

    @forumthread_post_view_check
    def get(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)

    @forumthread_post_view_check
    def post(self, request, *args, **kwargs):
        # 从内容找到提到的用户
        obj = self.get_object()

        mutable_post = request.POST.copy()
        mutable_post.setlist(
            'referenced', 
            [str(u.id) for u in get_ref_user(mutable_post['content'])]) 

        form = self.get_form_class()(mutable_post, instance=obj, 
                                     initial=self.get_initial())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.get_top()
        self.object = form.save()

        form.send_notifications()
        form.handle_perm()
        return super().form_valid(form)

    def get_success_url(self,):
        obj = self.get_object()
        assert(obj)
        return obj.get_absolute_url()

    def required_deleted(self,):
        '''如果不是一楼，就看reply是不是被删除。否则返回False。'''
        assert self.request 
        if 'reply_pk' in self.kwargs:
            obj = self.model.objects.get(id=self.kwargs['reply_pk'])
            return obj.deleted
        return  False


class ForumThreadCreateView(ForumThreadBaseView):
    pass


class ForumThreadUpdateView(ForumThreadBaseView):
    pass


class ForumThreadReplyCreateView(ForumThreadBaseView):
    is_new = False


class ForumThreadReplyUpdateView(ForumThreadBaseView):
    is_new = False


# === 微贴 ===


class MicroForumThreadDetailView(DetailView):
    model = MicroForumThread


class MicroForumThreadCreateView(LoginRequiredMixin, CreateView):
    model = MicroForumThread
    form_class = MicroForumThreadCreateForm