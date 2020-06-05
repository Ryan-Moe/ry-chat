from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
class Thread(models.Model):
    title = models.CharField(max_length = 256)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return 'Thread: %s' % self.title

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return '%s @ %s: %s' % (self.author.username, self.date, self.text[:100])
