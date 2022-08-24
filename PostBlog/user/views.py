from tokenize import Token

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from user.forms import SignUpForm, UpdateForm, SetNewPasswordForm, GroupForm
from user.models import User, STAFF
from user.serializers import UserSerializer, LoginSerializers


class LoginAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": status.HTTP_200_OK, "Token": token.key})


class SignUpView(CreateView):
    """This view should create users."""
    form_class = SignUpForm
    success_url = reverse_lazy('user:login')
    template_name = 'registration/signup.html'


class UserRegistration(CreateAPIView):
    serializer_class = UserSerializer
    template_name = 'registration/signup.html'
    queryset = User.objects.all()


class ProfileView(CreateView):
    """This view should display profile view according to user."""
    form_class = SignUpForm
    template_name = "registration/profile.html"


class Upadate(LoginRequiredMixin, UpdateView):
    """This view should update user profile."""
    model = User
    form_class = UpdateForm
    template_name = "registration/update.html"
    success_url = reverse_lazy("user:profile")


class SetNewPassword(PasswordResetConfirmView):
    """This view should help to reset user's password."""
    form_class = SetNewPasswordForm


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """It should delete user form User model."""

    model = User
    success_url = reverse_lazy('user:signup')


class AddUserView(LoginRequiredMixin, CreateView):
    """Manager can add users,so added users called staff members."""

    form_class = SignUpForm
    template_name = "registration/adduser.html"
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        """if manager add any user then manager id will store in user field otherwise user id will store"""
        product = form.save(commit=False)

        product.user = self.request.user

        product.user_type = STAFF
        product.parent = self.request.user

        product.save()
        return redirect('blog:home')


class ShowUser(LoginRequiredMixin, ListView):
    """It should use to filter queryset."""
    template_name = "registration/showuser.html"
    context_object_name = "your_user"
    success_url = reverse_lazy('blog:home')

    def get_queryset(self, **kwargs):
        """It should filter queryset and display users list by their manager."""
        return User.objects.filter(parent=self.request.user.id)


class UserDelete(LoginRequiredMixin, DeleteView):
    """Manager delete their staff members"""
    model = User
    success_url = reverse_lazy('blog:home')

    def get(self, request, *args, **kwargs):
        """after successfully deleted staff members it redirects to manager's home page"""
        print(self.request.user.id)
        self.get_object().delete()
        return redirect(self.success_url)


class UpadateStaff(LoginRequiredMixin, UpdateView):
    """user profile update"""
    model = User
    form_class = UpdateForm
    template_name = "registration/staff_update.html"
    success_url = reverse_lazy("user:show_user")


class GroupView(LoginRequiredMixin, CreateView):
    """permission update and delete"""
    model = Group
    form_class = GroupForm
    template_name = "registration/permission.html"
    success_url = reverse_lazy("blog:home")


class GroupList(LoginRequiredMixin, ListView):
    """user see all the groups."""
    template_name = 'registration/group.html'
    context_object_name = 'group_listing'

    def get_queryset(self):
        return Group.objects.order_by('name')


class UpdatePermission(LoginRequiredMixin, UpdateView):
    """User update group permission"""
    model = Group
    form_class = GroupForm
    template_name = "registration/permission_update.html"
    success_url = reverse_lazy("blog:home")


class DeletePermission(LoginRequiredMixin, DeleteView):
    """user delete permission"""
    model = Group
    success_url = reverse_lazy("blog:home")

    def get(self, request, *args, **kwargs):
        """ater delete the permission it redirect to home page"""
        self.get_object().delete()
        return redirect(self.success_url)
