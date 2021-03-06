from django.db.models import Q
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from modules.node.models import Nodes
from modules.read.models import Readings
from modules.user.models import Staffs



class NodeListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('node_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)


	class Meta:
		model 		= 	Nodes
		fields 		= 	'__all__'


class NodeCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	Nodes
		exclude 	= 	['created_at','updated_at']


class NodeRetrieveSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('node_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	read 				= 	SerializerMethodField('get_read')

	def get_read(self, obj):
		request 			= 	self.context.get('request')
		listerStart 		= 	int(request.GET.get('listerStart', 0))
		listerLimit 		= 	int(request.GET.get('listerLimit', 25))
		offset 				= 	listerStart*listerLimit
		qstring 			= 	request.GET.get('queryString', '')
		readings 			= 	{}
		many 				=	True
		if len(qstring) == 0:
			readings 			=	Readings.objects.filter(node=obj).order_by('-created_at')[offset:offset+listerLimit]
		elif len(qstring) > 1:
			readings 			=	Readings.objects.filter(node=obj, created_at__icontains=qstring).order_by('-created_at')[offset:offset+listerLimit]	
		else:
			readings 			=	Readings.objects.filter(node=obj).order_by('-created_at')[0]
			many 				= 	False
			
		serializer_context 	= 	{'request': request }
		serializer 			= 	ReadingListSerializer(readings, many=many, context=serializer_context)
		return serializer.data

	class Meta:
		model 		= 	Nodes
		fields 		= 	'__all__'



class ReadingListSerializer(ModelSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.get('context', {}).get('request')
		str_fields = request.GET.get('read_fields', '') if request else None
		fields = str_fields.split(',') if str_fields else None
		super(self.__class__, self).__init__(*args, **kwargs)
		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	node 				= 	SerializerMethodField('get_node')
	#Reading 				= 	SerializerMethodField('get_Reading')

	def get_node(self, obj):
		request 			= 	self.context.get('request')
		serializer_context 	= 	{'request': request }
		nodes 				=	Nodes.objects.get(pk=obj.node.id)
		serializer 			= 	NodeRetrieveSerializer(nodes, context=serializer_context)
		return serializer.data


	class Meta:
		model 		= 	Readings
		fields 		= 	'__all__'


class ReadingCreateSerializer(ModelSerializer):
	class Meta:
		model 		= 	Readings
		exclude 	= 	['created_at','updated_at']


class StaffLoginSerializer(ModelSerializer):
	class Meta:
		model 		= 	Staffs
		exclude 	= 	['created_at','updated_at']

