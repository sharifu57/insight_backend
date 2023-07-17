from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *
       


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 2

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'content', 'attachment']
        depth = 2

     


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'content']
        