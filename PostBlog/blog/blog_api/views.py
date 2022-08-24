import datetime
import email

import django_filters
from allauth.account.utils import user_email
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from PostBlog.settings import EMAIL_HOST, EMAIL_HOST_USER
from blog.blog_api.filters import Searchfilter, DateFilter
from blog.blog_api.permissons import Blog_Permission,Comment_Permission
from blog.blog_api.task import comment_mail
from blog.models import Blog, Image, Comment
from blog.blog_api.serializers import BlogSerializer, ImageSerializer, CommentSerializer, UpdateSerializer
from like.like_api.serializer import LikeSerializer
from user.models import User


class BlogViewSet(ModelViewSet):
    """
    This Viewset should create blog,update blog,display detail of the blog,destroy blog,list of all blog.
    """
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated,Blog_Permission ]
    filter_class=Searchfilter

    # @action(detail=False, methods=["get"])
    # def index(self,request):
    #     send_email_task.delay('hello','hello',EMAIL_HOST_USER,'dhruvisapara@gmail.com')
    #     return Response('response done')

    @action(detail=True, methods=["post"], serializer_class=CommentSerializer)
    def comments(self, request, pk):
        """
        This method should save current user and blog id for comments
        """

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(blog_id=pk, comment=self.request.user)
        comment_mail.delay()
        return Response({'serializer': serializer.data})

    @action(detail=True, methods=["post"], serializer_class=LikeSerializer)
    def likes(self, request, pk):
        """
        This method should save current user and blog id for like
        """
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(blog_like_id=pk, user_like=self.request.user)
        return Response({'serializer': serializer.data})

    def create(self, request, *args, **kwargs):
        """
            This method is for creating the blog
        """
        print(self.request.user.user_type)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.user_type == User.STAFF:
            serializer.save(user_id=self.request.user.parent.id)
        serializer.save(user_id=self.request.user.id)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UserBlogViewSet(ModelViewSet):
    """
    This view should return current user published blog only
    """
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


class CommentViewSet(ModelViewSet):
    """
        This Viewset should create Comment,update comment,delete comment,list of all comment.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated,Comment_Permission ]


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     """
    #         This method is for creating the blog
    #     """
    #     serializer=self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     if self.request.user.user_type == "staff":
    #         serializer.save(user_id=self.request.user.parent.id)
    #     serializer.save(user_id=self.request.user.id)
    #
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     """
    #     This method is for listing all the blog
    #     """
    #
    #     serializer=self.get_serializer(self.get_queryset(),many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request,pk):
    #     """
    #     This method is for display detailed blog
    #     """
    #
    #     blog=Blog.objects.filter(pk=self.kwargs.get('pk'))
    #     serializer=self.get_serializer(blog,many=True)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, *args, **kwargs,):
    #     """
    #     This method should delete particular blog
    #     """
    #
    #     instance= Blog.objects.filter(pk=self.kwargs.get('pk'))
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def update(self, request, pk):
    #     # import pdb
    #     # pdb.set_trace()
    #     # blog_update=Blog.objects.filter(pk=self.kwargs.get('pk'))
    #     blog=get_object_or_404(Blog,pk=pk)
    #     serializer =self.get_serializer(data=request.data,blog=blog)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def update(self, request, pk,**kwargs):
    #     import pdb
    #     pdb.set_trace()
    #     partial = kwargs.pop('partial', False)
    #     # instance = Blog.objects.filter(pk=self.kwargs.get('pk'))
    #     instance=self.get_object_or_404(Blog,pk=pk)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return  Response(serializer.data)


# class DateList(ListAPIView):
#     """
#     This view should display all the blogs or serachfilter by user or title
#     """
#
#     serializer_class = BlogSerializer
#     permission_classes = [IsAuthenticated, ]
#     queryset = Blog.objects.all()
#     filter_class = DateFilter

# class AddBlogApiView(GenericAPIView):
#     """
#     Authenticated staff members can add blogs
#     for mangers and user can also add the blog
#     """
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = BlogSerializer
#
#     def get(self, request):
#         serializer = BlogSerializer(data=request.data)
#         serializer.is_valid()
#         # serializer.save()
#         return Response({'serializer': serializer.data})
#
#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(status=status.HTTP_201_CREATED, data=serializer.validated_data)
#
#     def post(self, request):
#         serializer = BlogSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         if self.request.user.user_type == "staff":
#             serializer.save(user_id=self.request.user.parent.id)
#         else:
#             serializer.save(user_id=self.request.user.id)
#
#         return Response({'serializer': serializer.data})


# class UserBlogApiview(GenericAPIView):
#     """
#     this view should return user's blog list and
#     for staff members manager's blod list will display
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = BlogSerializer
#
#     def get(self, request):
#         blogs = Blog.objects.filter(user=self.request.user.parent)
#         serializer = BlogSerializer(blogs, many=True)
#         return Response({"articles": serializer.data})

# class UpdateBlogApiView(GenericAPIView, UserPassesTestMixin):
#     """
#     staff members can update their manager's blog
#     """
#
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED, data=serializer.validated_data)
#
#     def post(self, request, pk):
#         profile = get_object_or_404(Blog, pk=pk)
#         serializer = UpdateSerializer(profile, data=request.data)
#         if not serializer.is_valid():
#             return Response({'serializer': serializer, 'profile': profile})
#         serializer.save()
#         return Response({'message': "successfully updated"}, status=status.HTTP_200_OK)

# def test_func(self,pk):
#     import pdb;
#     pdb.set_trace()
#     """if user is staff members then only they can  edit the blogs"""
#     obj = Blog.objects.get(pk=self.kwargs.get('pk'))
#
#     if self.request.user.user_type == "staff":
#         return self.request.user.parent_id == obj.user_id
#
#     return self.request.user.id == obj.user_id


# class ImageApiView(GenericAPIView):
#     """
#     show blog related images
#     """
#     model = Image
#     permission_classes = [IsAuthenticated]
#     serializer_class = ImageSerializer
#
#     def get(self, request, pk):
#         image = Image.objects.filter(blog_image=self.kwargs.get('pk'))
#         serializer = ImageSerializer(image, many=True)
#         return Response({"articles": serializer.data})


# class AddCommentsApiView(GenericAPIView):
#     """
#     add comments on blogs
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED, data=serializer.validated_data)

# def get(self, request, pk):
#     serializer = CommentSerializer()
#     return Response({'serializer': serializer})
#
# def post(self, request, pk):
#     serializer = CommentSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     if self.request.user.user_type == "staff":
#         serializer.save(comment_id=self.request.user.parent.id, blog_id=pk)
#     else:
#         serializer.save(comment_id=self.request.user.id, blog_id=pk)
#
#     return Response({'serializer': serializer.data})


# class DisplayCommentApiView(GenericAPIView):
#     """
#     display comments by blog
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = CommentSerializer
#
#     def get(self, request, pk):
#         blog_comment = Comment.objects.filter(blog=self.kwargs.get('pk'))
#         serializer = CommentSerializer(blog_comment, many=True)
#         return Response({"articles": serializer.data})


# class BlogUploadImageApiView(GenericAPIView):
#     """user can upload images for their published blog"""
#
#     permission_classes = [IsAuthenticated]
#     serializer_class = ImageSerializer
#     queryset = Image.objects.all()

# def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(status=status.HTTP_201_CREATED, data=serializer.validated_data)

# def post(self, request, pk, Format=None):
#     # import pdb;
#     # pdb.set_trace()
#
#     # profile = get_object_or_404(Image, pk=pk)
#     serializer = ImageSerializer(data=request.data['file'])
#     serializer.is_valid(raise_exception=True)
#     serializer.save(blog_image=pk)
#
#     return Response({'serializer': serializer})


# class DetailBlogApiView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BlogSerializer
#
#     def get(self, request, pk):
#         blogs = Blog.objects.filter(pk=self.kwargs.get('pk'))
#         serializer = BlogSerializer(blogs, many=True)
#         return Response({"articles": serializer.data})


# class UpdateImageApiView(GenericAPIView):
#     serializer_class = ImageSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Image.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED, data=serializer.validated_data)

# def get(self, request, pk):
#     profile = get_object_or_404(Image, pk=pk)
#     serializer = ImageSerializer(profile)
#     return Response({'serializer': serializer, 'profile': profile})

# def post(self, request, pk):
#     import pdb;
#     pdb.set_trace()
#     profile = get_object_or_404(Image, pk=pk)
#     serializer = ImageSerializer(profile, data=request.data)
#
#     if not serializer.is_valid():
#         return Response({'serializer': serializer, 'profile': profile})
#     serializer.save()
#     return redirect('blog:home')
#
# def put(self, request, pk):
#
#         device = self.get_object(pk)
#         serializer = ImageSerializer(device, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def put(self, request, *args, **kwargs):
#     serializer = ImageSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(Image, pk='pk')
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BlogDeleteApiview(GenericAPIView):
#     serializer_class = BlogSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, pk):
#         instance = Blog.objects.filter(pk=self.kwargs.get('pk'))
#         instance.delete()
#         return Response({'message': "successfully deleted blog"}, status=status.HTTP_200_OK)


# class ImageDeleteApiView(GenericAPIView):
#     serializer_class = ImageSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get(self, requets, pk):
#         instance = Image.objects.filter(blog_image=self.kwargs.get('pk'))
#         instance.delete()
#         return Response({'message': "successfully deleted image"}, status=status.HTTP_200_OK)
