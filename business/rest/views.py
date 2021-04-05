from django.shortcuts import render
from rest_framework import generics

from news.models import news, Images, Category
from users.models import UserData
from .serializers import (
    NewsSerializer, 
    UserDataSerializer, 
    UniqueIDSerializer, 
    ImageSerializer,
    CategorySerializer,
    CategoryNewsSerializer,
)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
from rest_framework.response import Response
# Response helps to return the data

from rest_framework.views import APIView 
# APIView supports requests (get/post)
# It is a wrapper that allows to create APIView

from rest_framework.permissions import AllowAny, IsAuthenticated

import uuid

class CSRFExemptMixin(object):
   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
       return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

# Inherits APIView with many methods such as get()
class TestView(generics.ListAPIView):
    
    queryset = news.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (IsAuthenticated,)
    
    # def get(self, request, *args, **kwargs):
    #     qs = news.objects.all()
    #     serializer = PostSerializer(qs, many=True)
    #     return Response(serializer.data)
    #     #return a response at the end of the request

    # def post(self, request, *args, **kwargs):
    #     serializer = PostSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

class ImageAPIView(generics.RetrieveAPIView):
    queryset = news.objects.all() 
    serializer_class = ImageSerializer

# @method_decorator(csrf_exempt, name='dispatch')
class LogDataView(CSRFExemptMixin, generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    # @csrf_exempt
    # def post(self, request):
    #     serializer = UserDataSerializer(data=request.data)

class UniqueIDAPIView(generics.ListAPIView):
    
    def get(self, request):
        id = uuid.uuid1()
        json_convert = {"userID": id}
        results = UniqueIDSerializer(json_convert).data
        return Response(results)

class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryNewsAPIView(generics.ListAPIView):
    # queryset = news.objects.filter()
    serializer_class = CategoryNewsSerializer

    def get_queryset(self):
        category_name = self.kwargs['slug']
        category_instance = Category.objects.get(slug = category_name)
        return news.objects.filter(category = category_instance)


