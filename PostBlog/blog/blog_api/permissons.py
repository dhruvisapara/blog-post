from rest_framework import permissions
from rest_framework.permissions import BasePermission


class Blog_Permission(BasePermission):
    message = "only author can update or delete the blogs"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class Comment_Permission(BasePermission):
    message = "you dont have approprite rights for this comment"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.comment == request.user
