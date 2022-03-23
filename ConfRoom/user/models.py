from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)  # if True, User is Admin else Employee

    def __str__(self):
        return self.username or "None"
