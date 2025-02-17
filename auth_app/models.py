from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_icons/', default='user_icons/standart_user.jpg')
    bio = models.CharField(max_length=256, blank=True)
    theme = models.BooleanField(default=False) # True=night | False=day

    def __str__(self):
        return self.username