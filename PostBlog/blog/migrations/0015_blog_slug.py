# Generated by Django 4.0.4 on 2022-08-24 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_blog_formset_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
