import json
import time
import datetime
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
#from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, get_list_or_404
from modules.read.models import Readings
from modules.serializers import ReadingCreateSerializer, ReadingListSerializer
from modules.node.models import Nodes


class ReadingViewSets(viewsets.ViewSet):
	authentication_classes  =   [TokenAuthentication]
	permission_classes      =   [IsAuthenticated]

	def list(self, request):
		listerStart 		= 	int(request.GET.get('listerStart', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit', 50))
		offset 				= 	listerStart*listerLimit
		qstring 			= 	request.GET.get('queryString', '')
		reads 				=	{}
		if len(qstring) > 0:
			reads 			=	Readings.objects.filter(created_at__icontains=qstring).order_by('-created_at')[offset:offset+listerLimit]	
		else:
			reads 				= 	Readings.objects.filter().order_by("-created_at")[offset:offset+listerLimit]
		serializers		    = 	ReadingListSerializer(reads, many=True, context={'request':request})
		return Response(serializers.data)


	def create(self, request):
		time.sleep(2)
		serializer = ReadingCreateSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, request, pk=None):
		try:
			queryset = Readings.objects.get(pk=pk)
			serializers = ReadingCreateSerializer(queryset, context={'request':request})
			return Response(serializers.data)
		except:
			Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):
		pass


	def partial_update(self, request, pk=None):
		pass


	def destroy(self, request, pk=None):
		pass



@api_view(['POST'])
@permission_classes([AllowAny])
def read_post(request, format=None):
	if request.method == 'POST':
		for d in request.data:
			node = Nodes.objects.get(chipid=d['c_id'])
			if node is not None:
				dnow = datetime.datetime.now()
				dt_string = dnow.strftime("%Y-%m-%d %H:%M:%S")
				time_threshold = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(hours=1)
				if Readings.objects.filter(Q(node=node) & Q(randid=d['r_id'])).exclude(created_at__lt=time_threshold).count() == 0:
					parse_data = { 'node': node.id, 'volt': d['volt'], 'amps': d['amps'], 'randid': d['r_id'], 'readed_at': dt_string}
					serializer = ReadingCreateSerializer(data=parse_data)
					if serializer.is_valid():
						serializer.save()
		return Response(status=status.HTTP_200_OK)
	else:
		pass
	return Response(status=status.HTTP_400_BAD_REQUEST)