from django.db import models
from rest_framework import serializers

from songs.models import Song, Comment, Tag, Album


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['content']

    def validate_content(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Length of a tag should not be more than 50")
        return value


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['name', 'file', 'likes', 'views', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'song']

    def save(self, user):
        comment = Comment(**self.validated_data)
        comment.user = user
        comment.save()
        return comment


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'public', 'user', 'followers', 'song']


class TagSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['name', 'file', 'likes', 'views', 'tag']
        tag_content = models.CharField(max_length=50)

    def validate(self, data):
        tag_content = data.get('tag_content', None)
        if tag_content == "":
            tag_content = None
        if tag_content is None:
            raise serializers.ValidationError("Tag content is required")
        return data

    def update(self, instance, validated_data):
        tag_content = validated_data.get('tag_content', None)
        tag, _ = Tag.objects.get_or_create(content=tag_content)
        instance.tag.add(tag)
        instance.save()
        return instance
