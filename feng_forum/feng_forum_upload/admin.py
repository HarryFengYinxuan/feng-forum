from django.contrib import admin

from .models import UploadedMedia

# Register your models here.
admin.site.register(UploadedMedia, admin.ModelAdmin)