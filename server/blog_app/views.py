from rest_framework import viewsets, permissions, pagination, filters, generics
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CreateUserSerializer, UserSerializer, CommentSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    ordering = 'added_at'


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-added_at')
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberSetPagination


class CreateUserView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан',
        })


class UserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug').lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post).order_by('-added_at')

    def post(self, request, post_slug):
        serializer = self.get_serializer(data={
            'post': post_slug,
            'author': request.user,
            'text': request.data.get('text'),
        })
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({
            'comment': self.get_serializer(comment, context=self.get_serializer_context()).data,
            'message': 'Комментарий успешно отправлен',
        })
