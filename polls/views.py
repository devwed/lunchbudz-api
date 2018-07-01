from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from polls.models import User, Group, Membership
from polls.serializers import UserSerializer, GroupSerializer, MembershipSerializer

@csrf_exempt
def users(request):
	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = UserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
	try:
		user = User.objects.get(pk=pk)
	except User.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = UserSerializer(user)
		return JsonResponse(serializer.data)

@csrf_exempt
def groups(request):
	if request.method == 'GET':
		groups = Group.objects.all()
		serializer = GroupSerializer(groups, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = GroupSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def group_detail(request, pk):
	try:
		group = Group.objects.get(pk=pk)
	except Group.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = GroupSerializer(group)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		name = data.get('name')
		if isinstance(name, str):
			try:
				user = User.objects.get(name=name)
			except User.DoesNotExist:
				return HttpResponse(status=400)
			if not Membership.objects.filter(user=user, group=group).exists():
				membership = Membership(user=user, group=group)
				membership.save()
			return HttpResponse(status=200)
		return HttpResponse(status=400)

@csrf_exempt
def ready(request, pk):
	try:
		group = Group.objects.get(pk=pk)
	except Group.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'PUT':
		data = JSONParser().parse(request)
		name = data.get('name')
		if isinstance(name, str):
			try:
				user = User.objects.get(name=name)
			except User.DoesNotExist:
				return HttpResponse(status=400)
			try:
				membership = Membership.objects.get(user=user, group=group)
			except Membership.DoesNotExist:
				return HttpResponse(status=400)
			membership.ready = True
			membership.save()
			#now see if all members are ready, and if so flip group to ready
			if all_ready(group):
				group.ready = True
				group.save()
			return HttpResponse(status=200)
		return HttpResponse(status=400)

	elif request.method == 'GET':
		memberships = Membership.objects.filter(group=group)
		serializer = MembershipSerializer(memberships, many=True)
		return JsonResponse(serializer.data, safe=False)


#Purpose: checks to see if all group members are ready
#Output: True || False
#Conditions: needs to only be called with valid, member-having 
#group or will set group to ready
def all_ready(group):
	ready = True
	members = Membership.objects.filter(group=group)
	for member in members:
		if not member.ready:
			ready = False
			break
	return ready 