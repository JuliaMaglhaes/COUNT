from rest_framework import generics
from .serializers import CountSerializer
from counteye.models import Count
# from django.shortcuts import render

class CountList(generics.ListCreateAPIView):
    queryset = Count.postobjects.all()
    serializer_class = CountSerializer

class CountDetail(generics.RetrieveDestroyAPIView): #RetrieveAPIView?
    queryset = Count.objects.all()
    serializer_class = CountSerializer