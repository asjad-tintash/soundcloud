from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from songs.api.serializers import TagSerializer, SongSerializer, CommentSerializer, AlbumSerializer
from songs.models import Song, Comment, Tag, Album
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import json

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



class SongViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # filter_backends = (DjangoFilterBackend,)


    def get_queryset(self):
        song_name = self.request.query_params.get('song_name', None)
        tag_content = self.request.query_params.get('tag', None)
        if song_name is "":
            song_name = None
        if tag_content is None:
            tag_content = None
        if song_name is None and tag_content is None:
            return super().get_queryset()
        queryset = Song.objects.all()
        if song_name is not None:
            return queryset.filter(name__startswith=song_name)

        if tag_content is not None:
            tags = Tag.objects.all()
            tag = tags.filter(content=tag_content)
            tag_id = str(tag[0].id)
            return queryset.filter(tag=tag_id)



    def create(self, request, *args, **kwargs):
        if request.user.is_admin:
            super().create(request)
            return Response({"message": "song added successfully"}, status=200)
        else:
            return Response({"message": "You don't have permission to add songs"}, status=403)

    def tag_song(self, request, *args, **kwargs):
        # if not request.user.is_admin:
        #     return Response({"Error": "Only admin can add tags"}, status=403)
        song_id = request.data.get('song_id', None)
        tag_ = request.data.get('tag_id', None)
        song = Song.objects.get(id=song_id)
        if isinstance(tag_, int):
            tag = Tag.objects.get(id=tag_)
        if isinstance(tag_, str):
            tag = Tag(content=tag_)
            tag.save()
        if tag and song:
            song.tag.add(tag)
            serializer = SongSerializer(song)
            return Response({"data": serializer.data}, status=200)
        else:
            return Response({"error": "Enter a valid song or tag id"})




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('song',)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        song_id = self.request.query_params.get('song_id', None)
        print(song_id)
        if song_id is None:
            return super().get_queryset()
        queryset = Comment.objects.all()
        return queryset.filter(song=song_id)

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        data = {}
        data['content'] = self.request.data['content']
        data['song'] = self.request.data['song']
        data['user'] = self.request.user.id
        print(data)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': 'added comment successfuully'}
            return Response(data, status=200)
        else:
            return Response(serializer.validation_errors)

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer



