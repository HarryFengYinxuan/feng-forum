# Generated by Django 3.0.2 on 2020-07-01 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feng_forum_user', '0004_auto_20200701_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
    ]