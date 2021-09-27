from rest_framework import serializers
from .models import Blog, Category

# Add your Serializers here


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class BlogSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Blog
        fields = [
            'user', 'category', 'title', 'slug', 'created_at', 'updated_at'
        ]


class ABlogSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Blog
        fields = [
            'user', 'category', 'title', 'slug', 'body', 'views', 'meta_title',
            'meta_desc', 'created_at', 'updated_at', 'youtube_link'
        ]
