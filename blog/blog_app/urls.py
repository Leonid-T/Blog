from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

app_name = 'blog_app'
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('comment/<slug:post_slug>', views.CommentView.as_view()),
]