from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from polls.models import User, Group, Membership
from polls.serializers import UserSerializer, GroupSerializer

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
			return HttpResponse(status=200)
		return HttpResponse(status=400)