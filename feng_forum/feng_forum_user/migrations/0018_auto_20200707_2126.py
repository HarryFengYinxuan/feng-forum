# Generated by Django 3.0.2 on 2020-07-07 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0017_auto_20200707_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, verbose_name='信息链接'),
        ),
    ]
