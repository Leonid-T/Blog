from rest_framework import viewsets, permissions, pagination, filters
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


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
