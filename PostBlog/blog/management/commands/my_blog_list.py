from django.core.management.base import BaseCommand

from blog.models import Blog
from inlineformset.models import Ingredients, Recipe


class Command(BaseCommand):
    help = 'User Blog List'

    def add_arguments(self, parser):
        parser.add_argument('user', nargs='+', type=str, help='User blog list')

    def handle(self, *args, **kwargs):
        user_blogs = kwargs['user']

        for user_blog in user_blogs:

            blog_list = Blog.objects.filter(user__username=user_blog)
            if blog_list.exists():
                list_of_user_blogs = list((blog_list.values_list('title', flat=True)))

                self.stdout.write(self.style.SUCCESS(
                    'Hello %s \n Below is your published blog_list \n %s ' % (
                       user_blogs,  list_of_user_blogs)))
            else:
                self.stdout.write(self.style.WARNING(' Sorry %s you are not published any blogs.' % user_blog))
