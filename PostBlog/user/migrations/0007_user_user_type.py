# Generated by Django 4.0.4 on 2022-04-29 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_profileimage_user_profile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('manager', 'manager'), ('staff', 'staff'), ('author', 'author')], default='author', max_length=8),
        ),
    ]
