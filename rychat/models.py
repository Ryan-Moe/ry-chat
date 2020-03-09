from django.db import models

# Create your models here.
class Thread(models.Model):
    title = models.CharField(max_length = 256)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.CharField(max_length = 32)

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.CharField(max_length = 32)
