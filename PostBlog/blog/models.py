from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from user.models import User

Rating = [
    ('b', 'Bad'),
    ('a', 'Average'),
    ('e', 'Excellent')
]


class Blog(models.Model):
    """This model contains all information about blogs"""
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now, null=True)
    description = models.TextField(blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    highlights = models.CharField(max_length=500, default=None)
    formset_image = models.ImageField(upload_to='images', null=True, blank=True)
    slug = models.SlugField(null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=(
                                        (1, 'Active'), (0, 'Inactive')
                                    ))
    rating = models.CharField(max_length=1, choices=Rating, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blogs"

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)
        from PIL import Image
        imag = Image.open(self.formset_image.path)
        output_size = (150, 25)
        imag.thumbnail(output_size)
        imag.save(self.formset_image.path)


class Comment(models.Model):
    """particular blog has many comments"""

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class Image(models.Model):
    """for one blog there are many related images"""
    blog_image = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='image')
    post_image = models.ImageField(upload_to='images', null=True, blank=True)
