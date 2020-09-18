from django.db import models
from user.models import User


class Tag(models.Model):
    content = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.content


class Song(models.Model):
    name = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to="media", max_length=50)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.CharField(max_length=300)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]


class Album(models.Model):
    title = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    followers = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)

    def __str__(self):
        return self.title
