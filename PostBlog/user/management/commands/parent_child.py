from django.core.management.base import BaseCommand

from inlineformset.models import Ingredients, Recipe
from user.models import User


class Command(BaseCommand):
    help = 'Parent Child'

    def add_arguments(self, parser):
        parser.add_argument('parent', nargs='+', type=str, help='Recipe Title')

    def handle(self, *args, **kwargs):
        parent = kwargs['parent']
        for child in parent:
            children = User.objects.filter(parent__username=child)
            if children.exists():
                list_of_ingredients = list((children.values_list('username', flat=True)))

                self.stdout.write(self.style.SUCCESS(
                    'Hello manager %s \n staff list \n %s'
                     % (parent[0],list_of_ingredients[0])))
            else:
                self.stdout.write(self.style.WARNING('%s sorry there is no recipe  available.' % list_of_ingredients))


