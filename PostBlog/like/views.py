from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from like.models import Likes


class LikeView(LoginRequiredMixin, View):
    template_name = "like/add_like.html"

    def post(self, request, *args, **kwargs):
        """if user already liked that blog then new object is not created otherwise created"""
        blog_id = kwargs.get('pk')
        user_id = request.user.id
        print(Likes.objects.all().count())
        created = Likes.objects.get_or_create(blog_like_id=blog_id, user_like_id=user_id)
        if created:
            print("you liked")
        else:
            print("You already liked the blog")

        return JsonResponse({'message': 'successfully'})
