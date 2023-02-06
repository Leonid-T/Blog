from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, pagination, filters, generics, mixins, status
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'content': request.data.get('content'),
            'author': request.user,
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        request.data.pop('author', None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        return Comment.objects.filter(post=post).order_by('-added_at')

    def create(self, request, *args, **kwargs):
        post_slug = self.kwargs.get('post_slug')
        serializer = self.get_serializer(data={
            'post': post_slug,
            'author': request.user,
            'text': request.data.get('text'),
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
