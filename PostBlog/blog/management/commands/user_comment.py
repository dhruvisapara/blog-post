from django.core.management.base import BaseCommand

from blog.models import Comment, Blog
from inlineformset.models import Ingredients, Recipe
from user.models import User


class Command(BaseCommand):
    help = 'User Comment'

    def add_arguments(self, parser):
        parser.add_argument('user', nargs='+', type=str, help='User Comment')

    def handle(self, *args, **kwargs):
        user = kwargs['user']
        for comment in user:
            user_comment = Comment.objects.filter(comment__username=comment)
            blog = user_comment.values('blog_id')[0]
            blog_id = blog.get('blog_id')
            blog_title = Blog.objects.get(id=blog_id).title

            if user_comment.exists():
                list_of_comments = list((user_comment.values_list('body', flat=True)))
                self.stdout.write(self.style.SUCCESS(
                    'Hello  %s \n Your comment on %s \n is %s'
                    % (user[0], blog_title, list_of_comments[0])))

            else:
                self.stdout.write(self.style.WARNING('%s sorry there is no recipe  available.' % list_of_comments))
