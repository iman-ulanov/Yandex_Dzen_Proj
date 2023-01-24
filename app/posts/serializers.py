from django.db import IntegrityError
from rest_framework import serializers

from .models import Post, Comment, RatePost


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'date_of_post']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'author', 'date_of_create']


class RatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatePost
        fields = '__all__'
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            status_rate = validated_data.pop('rate')
            status_post = RatePost.objects.get(**validated_data)
            status_post.rate = status_rate
            status_post.save()
            instance = status_post
        return instance
