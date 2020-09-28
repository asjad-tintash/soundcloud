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
    filter_backends = (filters.SearchFilter, )
    search_fields = ['name', 'tag__content']

    # def destroy(self, request, *args, **kwargs):
    #     print("delete method called")

    def tag_song(self, request, *args, **kwargs):
        """
        function to add tags in a song
        """
        song_id = request.data.get('song_id', None)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"Error": "Song with this id does not exist"}, status=404)
        serializer = TagSongSerializer(Song, data=self.request.data, context={'request': request})
        serializer.is_valid()
        data = serializer.validate(request.data)
        serializer.update(song, data)
        return Response({"message": "Tag added successfully"}, status=200)

    def increment(self, song_id, field):
        """
        function to increment views or like count depending on the field type
        field can be view or like
        """
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
        """
        function to increase view counts of the song
        """
        try:
            song_id = self.request.data['song_id']
        except:
            return Response({"Error": "Please pass a valid song id"}, status=400)
        self.increment(song_id, "view")
        return Response({"Message": "Views incremented"}, status=200)

    def like_song(self, request, *args, **kwargs):
        """
        function to increase the like count of the song
        """
        try:
            song_id = self.request.data['song_id']
        except:
            return Response({"Error": "Please pass a valid song id"}, status=400)
        self.increment(song_id, "like")
        return Response({"Message": "Likes incremented"}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset provides endpoint to all Comment related API calls
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('song', )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        """
        function to save the user as comment owner at time of comment creation
        """
        serializer.save(self.request.user)


class AlbumViewSet(viewsets.ModelViewSet):
    """
        This viewset provides endpoint to all Album related API calls
        """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (IsAuthenticated, )

    def follow_album(self, request, *args, **kwargs):
        """
        function to add user as a follower of album and increase the follower count
        """
        user_id = self.request.user.id
        album_id = self.request.data.get('album_id', None)
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"Error": "Album with this id does not exist"}, status=404)

        album.followers += 1
        album.user.add(request.user)
        album.save()
        return Response({"Message": "Followed successfully"}, status=200)

    def add_song(self, request, *args, **kwargs):
        """
        function to add song in an album
        """
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
