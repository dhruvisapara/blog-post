from django.core.management.base import BaseCommand

from inlineformset.models import Ingredients, Recipe


class Command(BaseCommand):
    help = 'Recipe ingredients'

    def add_arguments(self, parser):
        parser.add_argument('--recipe_title', nargs='+', type=str, help='Recipe Title')
        parser.add_argument('--show_description', nargs='+', type=bool, help='Recipe description')

    def handle(self, *args, **kwargs):
        recipes_ingredient = kwargs['recipe_title']
        recipes_dis = kwargs['show_description']
        if not recipes_dis:
            for recipe_title in recipes_ingredient:
                ingredients = Ingredients.objects.filter(recipe__title=recipe_title)
                if ingredients.exists():
                    list_of_ingredients = list((ingredients.values_list('name', flat=True)))

                    self.stdout.write(self.style.SUCCESS(
                        'You search ingredients for "%s " to make your job easy\n'
                        ' here is the list of ingredients'
                        ' for making delecious %s \n\n %s' % (
                            recipes_ingredient[0], recipes_ingredient[0], list_of_ingredients)))
                else:
                    self.stdout.write(self.style.WARNING('%s sorry there is no recipe  available.' % recipe_title))

        elif recipes_dis:
            description = Recipe.objects.get(title=recipes_ingredient[0]).description
            self.stdout.write(
                self.style.SUCCESS('method to make delicious %s is\n%s' % (recipes_ingredient[0], description)))
