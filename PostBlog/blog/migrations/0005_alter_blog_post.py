# Generated by Django 4.0.4 on 2022-04-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='post',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images'),
        ),
    ]
