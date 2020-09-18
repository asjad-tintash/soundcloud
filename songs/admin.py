from django.contrib import admin
from songs.models import Song, Tag, Comment, Album
# Register your models here.

admin.site.register(Song)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Album)
