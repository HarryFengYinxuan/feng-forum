# Generated by Django 3.0.2 on 2020-07-02 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_main', '0003_auto_20200702_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumthread',
            name='reply_to',
            field=models.ForeignKey(blank=True, help_text='作为什么贴子的回复。', null=True, on_delete=django.db.models.deletion.CASCADE, to='feng_forum_main.ForumThread'),
        ),
    ]