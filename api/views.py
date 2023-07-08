from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models.query_utils import Q
from api.serializers import *
from rest_framework.authtoken.models import Token


# Create your views here.
@permission_classes((permissions.AllowAny,))
class UserLoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
   
        # Check if a user with the provided username or email exists
        if User.objects.filter(Q(username=username) | Q(email=email) | Q(username=email)).exists():
            user = authenticate(username=username, password=password) or authenticate(email=email, password=password)
            print("user is authenticated")
            print(user)
            if user is not None:
                if user.is_active:
                    serializer = UserSerializer(user, many=False)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            "token": token.key,
                            "user": serializer.data
                        }
                    )
                else:
                    return Response(
                        {
                            'status': status.HTTP_404_NOT_FOUND,
                            'message': 'Failed to login (not activated)'
                        }
                    )
            else:
                print("user=====", user)
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'Incorrect username or password'
                    }
                )
        else:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'User does not exist'
                }
            )
