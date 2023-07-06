from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login

# Create your views here.
@permission_classes((permissions.AllowAny,))
class UserLoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        print("****user details****")
        print(username)
        print(password)
        print("****password details****")

        if User.objects.filter(Q(username=username)|Q(email=username)).exists():
            user_obj = User.objects.filter(Q(username=username) | Q(email=username) | Q(email=email)).first()
            user = authenticate(username = user_obj.username, password = password)
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