from rest_framework import viewsets

from .models import Author
from .serializers import AuthorRegisterSerializer


class AuthorRegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet для создания авторов!
    """
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer

