from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CreateUserSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_repeat',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        password_repeat = validated_data.get('password_repeat')

        if password != password_repeat:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})

        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
