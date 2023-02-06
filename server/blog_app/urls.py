from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')
router.register('post/(?P<post_slug>[^/.]+)/comment', views.CommentViewSet, basename='comment')

app_name = 'blog_app'
urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.CreateUserView.as_view()),
    path('user/', views.UserView.as_view()),
    # path('post/<slug:post_slug>/comment/', views.CommentView.as_view()),
]