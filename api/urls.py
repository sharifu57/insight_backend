from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login', csrf_exempt(views.UserLoginView.as_view())),
    path('profiles', views.UserProfilesView.as_view()),
    path('register', views.RegisterUserView.as_view()),
    path('posts', views.getPosts.as_view()),
    path('create_post', views.AddPostView.as_view()),
    path('users', views.UsersView.as_view()),
    path('add_comment', views.CommentsByPost.as_view()),
    path('post/<int:pk>', views.ViewOnePost.as_view())
]