# Generated by Django 4.0.4 on 2022-04-26 05:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_rename_image_image_post_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='like',
            field=models.SmallIntegerField(blank=True, choices=[(1, '👍️'), (-1, '👎️')], null=True),
        ),
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('user_like', 'blog_like')},
        ),
    ]