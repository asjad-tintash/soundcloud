import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated

from songs.api.serializers import (
    TagSerializer,
    SongSerializer,
    CommentSerializer,
    AlbumSerializer,
    TagSongSerializer,
)
from songs.models import Song, Comment, Tag, Album, Notification
from user.models import User
from songs.api.SongPermission import SongCreatePermission


class TagViewSet(viewsets.ModelViewSet):
    """
    This is the viewset for the Tag model
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    This is the viewset for the Tag model
    """
    permission_classes = (SongCreatePermission, )
    '''
    permission_classes_by_action = {
        'default': [IsAuthenticatedOrReadOnly],
        'create': [SongCreatePermission],
    }
    '''
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'tag__content']

    def tag_song(self, request, *args, **kwargs):
        song_id = request.data.get('song_id', None)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"Error": "Song with this id does not exist"}, status=404)
        serializer = TagSongSerializer(Song, data=self.request.data)
        serializer.is_valid()
        data = serializer.validate(request.data)
        serializer.update(song, data)
        return Response({"message": "Tag added successfully"}, status=200)

    def increment(self, song_id, field):
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"Error": "Song with this id does not exist"}, status=404)
        if field == "view":
            song.views += 1
        if field == "like":
            song.likes += 1
        song.save()

    def view_song(self, request, *args, **kwargs):
        try:
            song_id = self.request.data['song_id']
        except:
            return Response({"Error": "Please pass a valid song id"}, status=400)
        self.increment(song_id, "view")
        return Response({"Message": "Views incremented"}, status=200)

    def like_song(self, request, *args, **kwargs):
        try:
            song_id = self.request.data['song_id']
        except:
            return Response({"Error": "Please pass a valid song id"}, status=400)
        self.increment(song_id, "like")
        return Response({"Message": "Likes incremented"}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('song',)
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(self.request.user)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated, )

    def follow_album(self, request, *args, **kwargs):
        user_id = self.request.user.id
        album_id = self.request.data.get('album_id', None)
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"Error": "Album with this id does not exist"}, status=404)
        user = User.objects.get(id=user_id)

        album.followers += 1
        album.user.add(user)
        album.save()
        return Response({"Message": "Followed successfully"}, status=200)

    def add_song(self, request, *args, **kwargs):
        album_id = self.request.data['album_id']
        album = Album.objects.get(id=album_id)
        album_users = album.user.all()
        if not request.user == album.owner:
            return Response({"Message": "Only owner can add songs"})
        song_id = self.request.data['song_id']
        song = Song.objects.get(id=song_id)
        album.song.add(song)
        album.save()
        # generating notification
        message = song.name + " has been added to album " + album.title
        notification = Notification(message=message)
        notification.save()
        for user in album_users.iterator():
            notification.user.add(user)
        notification.save()
        return Response({"message": "Song added successfully"})
