from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = 'No profile image found.'

    def handle(self, *args, **kwargs):
        has_no_profile = User.objects.filter(profile_image__iexact='')
        list_of_users = list((has_no_profile.values_list('username', flat=True)))
        no_profile_count = has_no_profile.count()

        self.stdout.write(self.style.SUCCESS(
            '%s students are not upload their profile \n Below is the list of user that has no profile image \n %s' % (
               no_profile_count, list_of_users)))
