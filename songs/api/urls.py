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
    # path('comment/<int:song_id>', '')
]