from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS,  IsAuthenticated, DjangoModelPermissions, BasePermission
from .serializers import CountSerializer
from counteye.models import Count

from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
# from django.shortcuts import render

class PermissionUserCount(BasePermission):
    message = 'Somente autores do envio'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


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