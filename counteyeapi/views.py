from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, DjangoModelPermissions, BasePermission
from .serializers import CountSerializer
from counteye.models import Count
# from django.shortcuts import render

class PermissionUserCount(BasePermission):
    message = 'Somente autores do envio'
    def haspermission(self, request, v, x):
        if request.method in SAFE_METHODS:
            return True
        return x.author == request.user

class CountList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Count.postobjects.all()
    serializer_class = CountSerializer

class CountDetail(generics.RetrieveUpdateDestroyAPIView, PermissionUserCount ): #RetrieveDestroyAPIView?
    permission_classes = [DjangoModelPermissions]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class CreateCount(generics.CreateAPIView):
    queryset = Count.objects.all()
    serializer_class = CountSerializer