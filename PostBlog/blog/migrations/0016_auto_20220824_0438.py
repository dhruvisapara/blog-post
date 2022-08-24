# Generated by Django 4.0.4 on 2022-08-24 04:38

from django.db import migrations
from django.utils.text import slugify

from blog.models import Blog


def slugify_title(apps, schema_editor):
    '''
    We can't import the Blog model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    Blog = apps.get_model('blog', 'Blog')
    for post in Blog.objects.all():
        post.slug = slugify(post.title)
        post.save()


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0015_blog_slug'),
    ]

    operations = [

        migrations.RunPython(slugify_title),
    ]
