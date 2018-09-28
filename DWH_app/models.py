from django.db import models
from datetime import datetime
# Create your models here.

class Searches(object):
	"""docstring for searches"""
	search_key = models.CharField(max_length=200)
	created_at = models.DateTimeField(default=datetime.now, blank=True);
