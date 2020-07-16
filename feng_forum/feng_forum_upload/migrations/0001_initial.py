# Generated by Django 3.0.2 on 2020-07-02 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feng_forum_upload.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to=feng_forum_upload.models.user_upload_path, verbose_name='上传的文件')),
                ('uploaded_img', models.ImageField(blank=True, null=True, upload_to=feng_forum_upload.models.user_upload_path, verbose_name='上传的图像')),
                ('uploaded_vid', models.ImageField(blank=True, null=True, upload_to=feng_forum_upload.models.user_upload_path, verbose_name='上传的视频')),
                ('is_icon', models.BooleanField(default=False, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]