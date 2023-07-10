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
        
        print(email)
        print(username)
        print(password)
   
        # Check if a user with the provided username or email exists
        if User.objects.filter(Q(username=username) | Q(email=email) | Q(username=email)).exists():
            user = authenticate(username=username, password=password) or authenticate(email=email, password=password)
            print("user is authenticated")
            print(user)
            if user is not None:
                if user.is_active:
                    user_serializer = UserSerializer(user, many=False)
                    profile_serializer = ProfileSerializer(user.profile)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            "token": token.key,
                            "user": user_serializer.data,
                            "profile": profile_serializer.data
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
            
@permission_classes((permissions.AllowAny,))
class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        
        if not email or not password or not username:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email, Username or Password are required'
                }
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': 'Email Already Exists'
                }
            )
            
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    'status': status.HTTP_409_CONFLICT,
                    'message': "Username does not Exists"
                }
            )
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
        
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e)
                }
            )
            
        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': "User created Successfully"
            }
        )
        

@permission_classes((permissions.AllowAny,))
class UserProfilesView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({'data': serializer.data})
    
@permission_classes((permissions.AllowAny,))
class getPosts(APIView):
    def get(self, request):
        posts = Post.objects.filter(is_active=True, is_deleted=False).order_by('-created')
        serializer = PostSerializer(posts, many=True)
        return Response({'data': serializer.data})