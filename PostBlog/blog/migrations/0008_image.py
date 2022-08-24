# Generated by Django 4.0.4 on 2022-04-22 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_blog_about_writer_remove_blog_writer_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('blog_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='blog.blog')),
            ],
        ),
    ]
