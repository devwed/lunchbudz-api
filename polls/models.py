from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
class Group(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, blank=True, default='')
	members = models.ManyToManyField(User)
	ready = models.BooleanField(default=False)
	def __str__(self):
		return self.name
class Choice(models.Model):
	name = models.CharField(max_length=50)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

#class Membership to tie user to group, and have 1to1 for votes