from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import telebot

from .models import Post, Comment, RatePost
from accounts.models import Author
from .permissions import OwnerPermission, RatePermission
from .serializers import PostSerializer, CommentSerializer, RatePostSerializer

bot = telebot.TeleBot("5754591651:AAFyiK1RwrJaLwJrIDmSlFqYh0Gha95PPn8", parse_mode=None)

CHAT_ID_LIST = [
    '694537940'
]


def send_telegram_message(telegram_chat_id, message):
    for chat_id in telegram_chat_id:
        bot.send_message(chat_id, message)




class PostViewSet(viewsets.ModelViewSet):

    """
    ViewSet для просмотра, создания, удаления, изменения постов.
     Изменять и удалять пост могут только владельцы или админы(is_staff=True)
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnerPermission, ]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            text=self.kwargs.get('text'),
                        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user.author)
        headers = self.get_success_headers(serializer.data)
        send_telegram_message([self.request.user.author.telegram_chat_id, ], f'Post was successfully created.')
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API для просмотра и создания комментариев.
     Создавать могут даже неавторизованниые пользователи
     (в этом случае им будет привязан 1 автор, который будет временным юзером)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(
                author=self.request.user.author,
                post_id=self.kwargs.get('post_id')
            )
        else:
            serializer.save(
                author=Author.objects.all().first(),
                post_id=self.kwargs.get('post_id')
            )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API для изменения и удаления комментариев.
    Изменять и удалять комментарии могут только админы(is_staff=True)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatePostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для оценки постов, каждый пользователь может изменить свою оценку!
    """
    queryset = RatePost.objects.all()
    serializer_class = RatePostSerializer
    permission_classes = [RatePermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(
                author=self.request.user.author,
                post_id=self.kwargs.get('post_id'),
            )
