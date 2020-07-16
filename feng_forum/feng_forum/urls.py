from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/main/topics/')),
    path('admin/', admin.site.urls),
    path('main/', include('feng_forum_main.urls')),
    path('user/', include('feng_forum_user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] 

urlpatterns += static(
    settings.STATIC_URL, 
    document_root=settings.STATIC_ROOT)
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)