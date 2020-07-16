from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notification
from .forms import NotificationFormSet

class NotificationUpdateView(LoginRequiredMixin, FormView):
    template_name = 'feng_forum_user/notification_form.html'
    model = Notification
    form_class = NotificationFormSet
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = context['form']
        return context

    def get_form(self, form_class=None):
        if self.request.POST:
            form = self.get_form_class()(
                self.request.POST,
                queryset=self.request.user.forumaccount.get_messages()
                )
        else:
            form = self.get_form_class()(
                queryset=self.request.user.forumaccount.get_messages()
                )
                
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
