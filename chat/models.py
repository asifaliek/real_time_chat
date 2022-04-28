from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import asyncio
from django.template.defaultfilters import slugify
from random import randint


class Room(models.Model):
    title = models.CharField(max_length=128)
    code = models.CharField(unique=True, max_length=256, blank=True, null=True)
    users = models.ManyToManyField(User)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='room_creator')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = self.title.replace(" ", "_").lower()
        exists = Room.objects.filter(code=self.code).exists()
        while exists:
            self.code += "-" + str(randint(1, 999))
            exists = Room.objects.filter(code=self.code).exists()
        super().save(*args, **kwargs)

    @property
    def group_name(self):
        return "room-%s" % self.id


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author', on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.author.username

    
