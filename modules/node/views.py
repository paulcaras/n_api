import json
import time
import datetime
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from modules.node.models import Nodes
from modules.read.models import Readings
from modules.serializers import NodeCreateSerializer, NodeListSerializer, NodeRetrieveSerializer

class NodesViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		time.sleep(0.500)
		qaction = request.GET.get('action', 'lister')
		qfilter = request.GET.get('filter', 'list-nodes')
		nodes = {}
		if qaction == 'lister':
			if qfilter == 'list-nodes':
				nodes = Nodes.objects.all().order_by('-created_at')
			elif qfilter == 'active-nodes':
				time_threshold = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=3)
				reads = Readings.objects.filter(created_at__gt=time_threshold).values_list('node_id', flat=True).distinct('node_id')
				nodes = Nodes.objects.filter(id__in=reads)
		elif qaction == 'finder':
			qstring = request.GET.get('queryString', '')
			nodes = Nodes.objects.filter(name__icontains=qstring)
		serializers = NodeListSerializer(nodes, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		serializer = NodeCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			nodes = Nodes.objects.get(pk=pk)
			serializers = NodeRetrieveSerializer(nodes, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)


	def update(self, request, pk=None):
		time.sleep(1)
		tran_chg = True if request.GET.get('tran_chg', '0') == '1' else False
		if tran_chg and Nodes.objects.filter(tran=request.data['tran']).count() >= 1:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		queryset        		=   Nodes.objects.get(pk=pk)
		serializer      		=   NodeCreateSerializer(instance=queryset, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def node_auth(request, format=None):
	if request.GET.get('nid') is not None:
		qstring = request.GET.get('nid')
		nodes = Nodes.objects.filter(chipid__exact=int(qstring))[0]
		serializers = NodeListSerializer(nodes, context={'request':request})
		return Response(serializers.data)
	return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def node_list(request, format=None):
	qnid = request.GET.get('nid')
	nodes = Nodes.objects.filter(chipid__exact=int(qnid))[0]
	serializers = NodeRetrieveSerializer(nodes, context={'request':request})
	return Response(serializers.data)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def node_last(request, format=None):
	qnid = request.GET.get('nid')
	nodes = Nodes.objects.filter(chipid__exact=int(qnid)).order_by('-created_at')[0]
	serializers = NodeRetrieveSerializer(nodes, context={'request':request})
	return Response(serializers.data)