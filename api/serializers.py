from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre


class SerializerSlugRelatedField(serializers.SlugRelatedField):
    def __init__(self, serializer: serializers.ModelSerializer, **kwargs):
        self.serializer = serializer
        super(SerializerSlugRelatedField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self.serializer.to_representation(obj)


class TitleSerializer(serializers.ModelSerializer):
    category = SerializerSlugRelatedField(
        serializer=CategorySerializer(),
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = SerializerSlugRelatedField(
        serializer=GenreSerializer(),
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )

    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'GET':
            return data
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title, pk=self.context['view'].kwargs.get('title_id'))
            author = self.context['request'].user
            if Review.objects.filter(title_id=title, author=author,).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на один объект.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
