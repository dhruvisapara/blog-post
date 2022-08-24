from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import utc

from inlineformset.models import Recipe


def now():
    return datetime.utcnow().replace(tzinfo=utc)


class Command(BaseCommand):
    help = 'Displays stats related to Recipes'

    def handle(self, *args, **kwargs):
        From = now() - timedelta(hours=5)
        To = now()

        recipes_published_in_last_5_hour = Recipe.objects.filter(
            published__gt=From, published__lte=To).count()
        total_recipe = Recipe.objects.all().count()
        self.stdout.write(self.style.SUCCESS("In last five hours %s recipes are published." %
                                             recipes_published_in_last_5_hour))
        self.stdout.write(self.style.SUCCESS("Total published recipes are %s" %
                                             total_recipe))
