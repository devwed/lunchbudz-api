from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __str__(self):
		return self.name
class Group(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100)
	members = models.ManyToManyField(User, through='Membership')
	ready = models.BooleanField(default=False)
	def __str__(self):
		return self.name
class Membership(models.Model):
	joined = models.DateTimeField(auto_now_add=True)
	ready = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.name + ' in ' + self.group.name + ':' + str(self.ready)

class Choice(models.Model):
	name = models.CharField(max_length=50)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
