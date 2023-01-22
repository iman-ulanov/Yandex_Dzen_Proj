from rest_framework import serializers
from .models import Author, User


class AuthorRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)
    password_2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ['user', ]

    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError('Введите пароль правильно')
        return data

    def validate_username(self, username):
        if len(username) < 8:
            raise serializers.ValidationError('Имя пользователя должно быть не менее 8 символов')
        return username

    def validate_email(self, email):
        if '@email.com' not in email:
            raise serializers.ValidationError('Не правильно введена почта')
        return email

    def create(self, validated_data):
        try:
            user = User(username=validated_data['username'])
            user.set_password(validated_data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удалось создать пользователя {e}')
        else:
            author = Author.objects.create(telegram_chat_id=validated_data['telegram_chat_id'],
                                           email=validated_data['email'], user=user)
        return author
