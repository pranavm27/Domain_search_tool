from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Controls (models.Model):
	belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
	havePRHunterAccount = models.CharField(max_length=512)
	sendUpdates = models.CharField(max_length=512)

class Campaigns(models.Model):
	"""docstring for searches"""
	belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, default=000)
	name = models.CharField(max_length=1024)
	campaign_type = models.CharField(max_length=1024)
	start = models.CharField(max_length=1024)
	end = models.CharField(max_length=1024)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	
class Searches(models.Model):
	"""docstring for searches"""
	search_key = models.CharField(max_length=1024)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	campaign_id = models.ForeignKey(Campaigns, on_delete=models.CASCADE, default=000)

class SearchResults(models.Model):
	"""docstring for searches"""
	search_key = models.ForeignKey(Searches, on_delete=models.CASCADE, default=000)
	result = models.CharField(max_length=1028, unique=True)
	is_valid = models.CharField(max_length=1024, default='true')
	added_on = models.DateTimeField(default=datetime.now, blank=True);