# Generated by Django 4.0.4 on 2022-04-26 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0011_rename_image_image_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.BooleanField(default=False)),
                ('blog_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_likes', to='blog.blog')),
                ('image_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_likes', to='blog.image')),
                ('user_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]