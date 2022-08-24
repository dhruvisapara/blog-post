import uuid

from django.db import models
from blog.models import Blog, Image
from user.models import User

UP = 1
DOWN = -1
VALUE_CHOICE = ((UP, "👍️"), (DOWN, "👎️"),)


class Likes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    like = models.SmallIntegerField(null=True, blank=True, choices=VALUE_CHOICE)
    blog_like = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_likes')
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    favorites = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_like', 'blog_like')

    def add_visit(self):
           return self.like.count()
