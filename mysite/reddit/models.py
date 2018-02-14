import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


# note: pub_date is not really used for Subreddit_Info, but is there
#       for reference

class Subreddit_Info(models.Model):
    diplay_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.display_name
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Reddit_Post(models.Model):
    subreddit = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    class Meta:
        unique_together = ["subreddit", "title", "pub_date"]
        