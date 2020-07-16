from django.contrib import admin

from .models import ForumThread, MicroForumThread, Topic


admin.site.register(Topic, admin.ModelAdmin)
admin.site.register(ForumThread, admin.ModelAdmin)
admin.site.register(MicroForumThread, admin.ModelAdmin)
