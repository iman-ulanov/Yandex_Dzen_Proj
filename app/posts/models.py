from django.db import models
from django.db.models import Avg

from accounts.views import Author


class Post(models.Model):
    text = models.CharField(max_length=255)
    date_of_post = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.avg_rate.aggregate(Avg('rate'))

    def __str__(self):
        return f'{self.author.user.username} - {self.text}'


class Comment(models.Model):
    text = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_of_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment {self.id} by {self.profile.user.username} to {self.tweet.id}'


class RatePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='avg_rate')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    rate = models.IntegerField(choices=choice)

    class Meta:
        unique_together = ['author', 'post']

    def __str__(self):
        return self.rate
