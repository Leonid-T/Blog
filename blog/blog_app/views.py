from rest_framework import viewsets, permissions, pagination, filters, generics
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, RegisterSerializer, UserSerializer, CommentSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_query_param = 'page_size'
    ordering = 'added_at'


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан',
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.order_by('-added_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post).order_by('-added_at')
