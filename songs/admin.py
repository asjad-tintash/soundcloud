from django.contrib import admin

from songs.models import Song, Tag, Comment, Album, Notification

admin.site.register(Song)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Album)
admin.site.register(Notification)
