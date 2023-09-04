from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # なりたい自分や抱負などを入れる
    dream = models.TextField(verbose_name="なりたい自分", max_length=200, blank=True, null=True)