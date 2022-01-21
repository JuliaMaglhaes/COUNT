from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS,AllowAny,  IsAuthenticated, DjangoModelPermissions, BasePermission
from .serializers import CountSerializer
from counteye.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render

class PermissionUserCount(BasePermission):
    message = 'Somente autores do envio'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class CountList(generics.ListAPIView):
    # permission_classes = [AllowAny]
    serializer_class = CountSerializer
    queryset = Count.postobjects.all()

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Count, slug=item)

    # def get_queryset(self):
    #     return Count.objects.all()

# class CountList(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Count.postobjects.all()
#     serializer_class = CountSerializer

class CountDetail(generics.RetrieveAPIView):
    serializer_class = CountSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Count, slug=item)

# class CountDetail(generics.RetrieveUpdateDestroyAPIView, PermissionUserCount ): #RetrieveDestroyAPIView?
#     permission_classes = [AllowAny]
#     queryset = Count.objects.all()
#     serializer_class = CountSerializer

# class CreateCount(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Count.objects.all()
#     serializer_class = CountSerializer

class CreateCount(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = CountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AdminCountDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class EditCount(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class DeleteCount(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

def get_frame():
    camera =cv2.VideoCapture(0) 
    while True:
        _, img = camera.read()
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    del(camera)
    
def indexscreen(request): 
    try:
        template = "templates/index.html"
        return render(request,template)
    except:
        print("error")

@gzip.gzip_page

def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"