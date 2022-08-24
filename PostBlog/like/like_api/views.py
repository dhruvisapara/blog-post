from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from like.like_api.serializer import LikeSerializer


class LikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = LikeSerializer

    def post(self, request,pk):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(blog_like_id=pk, user_like_id=self.request.user.id)
        return Response(serializer.data)


    # def post(self, request, *args, **kwargs):
    #     """if user already liked that blog then new object is not created otherwise created"""
    #     blog_id = kwargs.get('pk')
    #     user_id = request.user.id
    #     like, created = Likes.objects.get_or_create(blog_like_id=blog_id, user_like_id=user_id)
    #
    #     if created:
    #         print("you already liked")
    #     else:
    #         print("You liked the blog")
    #
    #     return
