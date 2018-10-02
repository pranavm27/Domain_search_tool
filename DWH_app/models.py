from django.db import models
from datetime import datetime


class Searches(models.Model):
	"""docstring for searches"""
	search_key = models.CharField(max_length=200)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	

class Campaigns(models.Model):
	"""docstring for searches"""
	name = models.CharField(max_length=200)
	campaign_type = models.CharField(max_length=200)
	start = models.CharField(max_length=200)
	end = models.CharField(max_length=200)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	
