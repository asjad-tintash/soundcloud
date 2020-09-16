from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_admin
