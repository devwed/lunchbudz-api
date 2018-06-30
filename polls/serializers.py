from rest_framework import serializers
from polls.models import User, Group

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name')

class GroupSerializer(serializers.ModelSerializer):
	members = UserSerializer(read_only=True, many=True)
	class Meta:
		model = Group
		fields = ('id', 'created', 'name', 'ready', 'members')
