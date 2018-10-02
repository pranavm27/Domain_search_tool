from django.db import models
from datetime import datetime

 # Create your models here.

class Searches(models.Model):
	"""docstring for searches"""
	search_key = models.CharField(max_length=200)
	created_on = models.DateTimeField(default=datetime.now, blank=True);
	
	# def save(self, *args, **kwargs):
	# 	if not self.slug:
	# 			self.slug = slugify(self.title)
	# 			super(Searches, self).save(*args, **kwargs)
