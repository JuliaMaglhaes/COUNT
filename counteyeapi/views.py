from rest_framework import generics
from .serializers import CountSerializer
from counteye.models import Count
# from django.shortcuts import render

class CountSerializer(generics.ListCreateAPIView):
    queryset = Count.postobjects.all()
    serializer_class = CountSerializer
    pass

class CountDetail(generics.RetrieveDestroyAPIView):
    pass