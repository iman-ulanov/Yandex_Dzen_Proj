from django.shortcuts import render
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer
from .permissions import PostPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)
