# Generated by Django 3.0.2 on 2020-07-02 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feng_forum_upload', '0002_auto_20200702_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedmedia',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploadedmedia_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
