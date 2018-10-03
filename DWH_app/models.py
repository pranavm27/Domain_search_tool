from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Campaigns(models.Model):
	"""docstring for searches"""
	belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, default=000)
	name = models.CharField(max_length=200)
	campaign_type = models.CharField(max_length=200)
	start = models.CharField(max_length=200)
	end = models.CharField(max_length=200)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	
class Searches(models.Model):
	"""docstring for searches"""
	search_key = models.CharField(max_length=200)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	campaign_id = models.ForeignKey(Campaigns, on_delete=models.CASCADE, default=000)
