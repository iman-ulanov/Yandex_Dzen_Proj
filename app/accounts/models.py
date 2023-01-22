from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    telegram_chat_id = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

