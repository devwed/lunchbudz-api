from rest_framework import serializers
from polls.models import User, Group, Membership

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'name')

class GroupSerializer(serializers.ModelSerializer):
	members = UserSerializer(read_only=True, many=True)
	class Meta:
		model = Group
		fields = ('id', 'created', 'name', 'ready', 'members')

class MembershipSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	group = GroupSerializer()
	class Meta:
		model = Membership
		fields = ('joined', 'ready', 'user', 'group')