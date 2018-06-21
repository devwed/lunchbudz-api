from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100)
class Group(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, blank=True, default='')
	members = models.ManyToManyField(User)
	ready = models.BooleanField()
