from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class tweet(models.Model):
	tweet_text = models.CharField(max_length = 200)
	username = models.ForeignKey(User,on_delete=models.CASCADE) 
	post_date = models.DateTimeField('date published')

	def __str__(self):
		return self.tweet_text

class base(models.Model):
	username = models.ForeignKey(User,on_delete=models.CASCADE) 
	following = models.CharField(max_length=50,null=True) 
	followers = models.CharField(max_length=50,null=True) 

	def __str__(self):
		return "%s %s %s" % (self.username,self.following,self.followers)

