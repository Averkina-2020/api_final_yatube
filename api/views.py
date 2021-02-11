from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from .models import Follow, Post, Group
from .serializers import (
    CommentSerializer,
    PostSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments

    def perform_create(self, serializer):
        get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ('post', 'get')
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post')
