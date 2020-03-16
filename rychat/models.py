from django.db import models

# Create your models here.
class Thread(models.Model):
    title = models.CharField(max_length = 256)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.CharField(max_length = 32)

    def __str__(self):
        return 'Thread: %s' % self.title

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1024)
    date = models.DateTimeField('date posted')
    author = models.CharField(max_length = 32)

    def __str__(self):
        return '%s @ %s: %s' % (self.author, self.date, self.text[:100])
