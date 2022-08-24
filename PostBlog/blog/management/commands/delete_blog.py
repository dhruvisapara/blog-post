from django.core.management.base import BaseCommand

from blog.models import Blog


class Command(BaseCommand):
    help = 'Delete blogs'

    def add_arguments(self, parser):
        parser.add_argument('blog_id', nargs='+', type=int, help='Blog ID')

    def handle(self, *args, **kwargs):
        blogs_ids = kwargs['blog_id']
        for blog_id in blogs_ids:
            try:
                blog = Blog.objects.get(pk=blog_id)
                blog.delete()
                self.stdout.write(self.style.SUCCESS('Blog "%s (%s)" deleted with success!' % (blog.title, blog_id)))
            except Blog.DoesNotExist:
                self.stdout.write(self.style.WARNING('Blog with id "%s" does not exist.' % blog_id))
