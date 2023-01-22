from django.db import models

from accounts.views import Author


class Post(models.Model):
    text = models.CharField(max_length=255)
    date_of_post = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.user.username} - {self.text}'


class Comment(models.Model):
    text = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id} by {self.profile.user.username} to {self.tweet.id}'