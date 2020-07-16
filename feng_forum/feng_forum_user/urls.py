from django.urls import path

from .views import NotificationUpdateView

urlpatterns = [
    path('notifications/', NotificationUpdateView.as_view(), 
         name='notification-list'),
]