from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, SongViewSet, CommentViewSet, AlbumViewSet

app_name = "songs"

router = DefaultRouter()
router.register('/tag', TagViewSet, )
router.register('/song', SongViewSet)
router.register('/comment', CommentViewSet)
router.register('/album', AlbumViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    # path('/comments_song/<int:song_id>', CommentViewSet.as_view({'get':'comments_song'})),
    path('/tag_song', SongViewSet.as_view({"post": "tag_song"})),
    path('/view_song', SongViewSet.as_view({"post": "view_song"})),
    path('/like_song', SongViewSet.as_view({"post": "like_song"})),
    path('/follow_album', AlbumViewSet.as_view({"post": "follow_album"})),
    path('/add_song', AlbumViewSet.as_view({"post": "add_song"})),
    # path('/song/<str:song_name>/<str:tag>', SongViewSet.as_view({'get':'search_song'}))
]
