from email.message import EmailMessage

from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from PostBlog.settings import EMAIL_HOST_USER
from user.models import User
from user.user_api.serializer import RegisterSerializer, MyTokenObtainPairSerializer,ChangePasswordSerializer, UserSerializer
from user.user_api.task import send_email_task


class UserViewSet(ModelViewSet):
    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = RegisterSerializer


class UserAPIView(CreateAPIView):
    permission_class = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


    # def get(self, request):
    #     import pdb
    #     pdb.set_trace()
    #     serializer = UserSerializer(request.user)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        send_email_task.delay()

        return Response("sent")

class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Logout(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         print(request.user)
#         logout(request)
#         return Response({"message": "LoggedOut"})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.user)
        try:
            access_token = request.data["access_token"]
            token = AccessToken(access_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get('username')
        user = User.objects.filter(username=username).first()

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({'user': user.username})
