from rest_framework import status, viewsets
from rest_framework.response import Response
from songs.api.serializers import TagSerializer, SongSerializer, CommentSerializer, AlbumSerializer
from songs.models import Song, Comment, Tag, Album
from rest_framework.permissions import IsAdminUser


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
