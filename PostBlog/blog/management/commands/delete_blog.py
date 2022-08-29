from django.core.management.base import BaseCommand

from blog.models import Blog


class Command(BaseCommand):
    help = 'Delete blogs'

    def add_arguments(self, parser):

        parser.add_argument('blog_title', nargs='+', type=str, help='Blog Title')

    def handle(self, *args, **kwargs):

        title = kwargs['blog_title']
        for blog_title in title:
            try:
                blog = Blog.objects.get(title=blog_title)
                blog.delete()
                self.stdout.write(self.style.SUCCESS(
                    'Blog "%s" Which is published on %s is deleted successfully!' % (blog.title, blog.pub_date)))
            except Blog.DoesNotExist:
                self.stdout.write(self.style.WARNING('Blog with title "%s" does not exist.' % blog_title))
