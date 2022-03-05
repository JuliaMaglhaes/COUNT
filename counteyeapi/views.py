from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS,AllowAny,  IsAuthenticated, DjangoModelPermissions, BasePermission
from .serializers import CountSerializer
from counteye.models import Count, ProductsRegister
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
from counteyeapi.services.count_IA import count_product
from counteyeapi.services.detection.detection import detection_product
from users.models import NewUser

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

# teste
class CountDetail(generics.RetrieveAPIView):
    serializer_class = CountSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Count, slug=item)

class CreateCount(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Count.objects.all()

    def post(self, request, format=None):
        serializer = CountSerializer(data=request.data)
        user_qualquer = NewUser.objects.first()

        if serializer.is_valid():
            count = serializer.save()
            predict = detection_product(serializer.validated_data["image"])
            xamount = count_product(serializer.validated_data["image"])
            count.amount = xamount
            count.product = predict["class"]
            count.author = user_qualquer
            count.save()
            acount=0

            for a in ProductsRegister.objects.filter(product=count.product):
                acount = a.amount               
               
            print(acount)
            t= ProductsRegister.amount
            # teste *
            ProductsRegister.objects.filter(product=count.product).update(product=count.product , amount = count.amount + acount)
     
            return Response({"produto":predict, "amount": xamount}, status=status.HTTP_200_OK)
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
    camera = cv2.VideoCapture(0) 

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