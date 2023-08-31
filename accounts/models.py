from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # なりたい自分や抱負などを入れる
    dream = models.TextField(max_length=100, blank=True, null=True)