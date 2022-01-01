from django.db import models
from modules.node.models import Nodes


class Readings(models.Model):
	node 				=	models.ForeignKey(Nodes, on_delete=models.SET_NULL, related_name='node', null=True)	
	volt				=	models.DecimalField(decimal_places=2, max_digits=8)
	amps				= 	models.DecimalField(decimal_places=2, max_digits=8)
	randid 				=   models.IntegerField(null=True, blank=True, default=0)
	readed_at 			=	models.DateTimeField()
	created_at 			= 	models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updated_at 			= 	models.DateTimeField(auto_now=True, blank=True, null=True)

	def __str__(self):
		return '%s' % (self.node.name)

	class Meta:
		db_table 				= 	"readings"
		verbose_name_plural		= 	"Readings"









