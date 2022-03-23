from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserSettingsSerializer, UserLoginSerializer
from room.serializers import UserInfoSerializer

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
# from django.contrib.auth import login, logout

from django.core.exceptions import ObjectDoesNotExist


class UserRegisterView(GenericAPIView):
    serializer_class = UserSettingsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, _ = Token.objects.get_or_create(user=user)
            response = {"status_code": status.HTTP_201_CREATED,
                        "message": "User successfully registered",
                        "result": serializer.data,
                        "token": token.key}
            return Response(response)

        else:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Some error occurred while registering user"}
            return Response(response)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                response = {"status_code": status.HTTP_200_OK,
                            "message": "User successfully logged in",
                            "result": serializer.data,
                            "token": token.key}
                # login(request, user)
                return Response(response)
            else:
                response = {"status_code": status.HTTP_400_BAD_REQUEST,
                            "message": "Username or password incorrect"}
                return Response(response)

        else:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Some error occurred while logging in user"}
            return Response(response)


class UserLogoutView(GenericAPIView):
    serializer_class = UserInfoSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()
            username = request.user.username
            response = {"status_code": status.HTTP_200_OK,
                        "message": "User successfully logged out",
                        "result": {
                            "username": username
                        }}
            # logout(request)
            return Response(response)
        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid token. User not logged in"}
            return Response(response)
