# Generated by Django 3.0.2 on 2020-07-01 18:27

from django.db import migrations, models
import feng_forum_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=feng_forum_user.models.user_icon_path),
        ),
    ]
