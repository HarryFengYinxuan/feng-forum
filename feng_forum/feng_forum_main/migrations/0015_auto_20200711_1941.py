# Generated by Django 3.0.2 on 2020-07-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_main', '0014_auto_20200708_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumthread',
            name='reply_to',
            field=models.ForeignKey(blank=True, help_text='作为什么贴子的回复。', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forumthread_replyto', to='feng_forum_main.ForumThread'),
        ),
        migrations.AlterField(
            model_name='forumthread',
            name='top_level',
            field=models.ForeignKey(blank=True, help_text='一楼', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forumthread_toplevel', to='feng_forum_main.ForumThread'),
        ),
    ]
