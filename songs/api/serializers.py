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
        fields = ['content', 'song', 'user']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'public', 'user', 'followers', 'song']
