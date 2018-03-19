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
    link = models.CharField(max_length=250, default='')
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    class Meta:
        unique_together = ["subreddit", "title", "pub_date"]


class Twitter_Post(models.Model):
    message = models.CharField(max_length=350, default='')
    username = models.CharField(max_length=100, default='')
    handle = models.CharField(max_length=100, default='')
    pub_date = models.CharField(max_length=100, default='')
    icon = models.CharField(max_length=200, default='')
    urls = models.CharField(max_length=3000, default='')
    hash = models.CharField(max_length=500, default='')
    mentions = models.CharField(max_length=2000, default='')
    searchQuery = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.message
    class Meta:
        unique_together = ["message", "handle", "username", "pub_date"]

class Youtube_Post(models.Model):
    ytid = models.CharField(max_length=20, default='')
    searchQuery = models.CharField(max_length=200, default='')
    def __str__(self):
        return self.ytid
    class Meta:
        unique_together = ["ytid", "searchQuery"]



class Saved_Post(models.Model):
    userid = models.IntegerField(default=-1)
    post_type = models.CharField(max_length=20, default='null')
    postid = models.IntegerField(default=-1)



    # note that default ID is -2, to avoid any accidents from
    #   setting Users to the default saved_post userid value of -1
class User_Info(models.Model):
    userid = models.IntegerField(default=-2)
    username = models.CharField(max_length=100, default='null')
