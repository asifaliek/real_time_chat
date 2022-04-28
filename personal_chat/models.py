
from django.db import models

# Create your models here.


class Thread(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    users = models.ManyToManyField('auth.User')

    def __str__(self) -> str:
        return f'From <Thread - {self.name}>'

class PersonalMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'