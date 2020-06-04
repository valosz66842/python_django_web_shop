
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Users,Limitedtime,Product

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        # fields = '__all__'
        fields=["name","password","email","phone","time","confirmed","account"]

class LimitedtimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Limitedtime
        fields='__all__'

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields=["url","title","srcset","sold","money","sell","stock","id"]
