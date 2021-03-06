from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from modules.node.views import NodesViewSets, node_auth, node_list, node_last
from modules.read.views import ReadingViewSets, read_post
from modules.user.views import staff_login, index_page

router = routers.DefaultRouter()
router.register(r'node', NodesViewSets, basename='nodes')
router.register(r'read', ReadingViewSets, basename='readings')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/p/read_post/', read_post),
    path('api/g/node_auth/', node_auth),
    path('api/g/node_list/', node_list),
    path('api/g/node_last/', node_last),
    path('api/login/', staff_login),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', index_page)
]
