from threading import Thread
from core.settings import BASE_DIR
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
from django.shortcuts import render, redirect
from counteyeapi.services.count_IA import count_product
from counteyeapi.services.detection.detection import detection_product
from users.models import NewUser
import os
import math
from .models import *
from django.core.paginator import Paginator
import concurrent.futures



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
            ProductsRegister.objects.filter(product=count.product).update(product=count.product , amount = count.amount + acount)
     
            return Response({"produto":predict, "amount": xamount}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AdminCountDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class EditCount(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class DeleteCount(generics.RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Count.objects.all()
    serializer_class = CountSerializer


COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
# class_names = [c.strip() for c in open('./counteyeapi/services/detection/names.names').readlines()]

# modelWeightsPath = "counteyeapi\services\detection\yolov3_training_last.weights"
# modelConfigurationPath = "counteyeapi\services\detection\yolov3_testing.cfg"
# net = cv2.dnn.readNet(modelConfigurationPath, modelWeightsPath)

class_names = [c.strip() for c in open('./counteyeapi/services/detection/names.names').readlines()]

modelWeightsPath = os.path.abspath('yolov3_training_last.weights')
modelConfigurationPath = os.path.abspath('yolov3_testing.cfg')

print(modelWeightsPath)

# "C:\Users\julia\OneDrive\Área de Trabalho\TCC\COUNT\counteyeapi\services\detection\yolov3_training_last.weights"
# "C:\Users\julia\OneDrive\Área de Trabalho\TCC\COUNT\counteyeapi\services\detection\yolov3_testing.cfg"

net = cv2.dnn.readNet(modelConfigurationPath, modelWeightsPath)

model = cv2.readNetFromDarknet(net)
model.setInputParams(size = (416, 416), scale=1/255)

def iteraip(object):
    for i in object:
        yield i

# @gzip.gzip_page
def dynamic_stream(request, descricao):
    
    # request, stream_path="video"
    results = []
    threads = {}
    ips = {}

    cameras = Cameras.objects.all()
    itera = iteraip(cameras)

    for i in range(cameras.count()):
        seila = next(itera)
        t = Thread(target = get_frame, args=(seila.ip, results))
        threads[seila.descricao] = t
        ips[seila.descricao] = seila.ip
        t.start()

    i = threads[descricao]
    i.join()
        
        # results.append(StreamingHttpResponse(get_frame(i,cameras[j].ip),content_type="multipart/x-mixed-replace;boundary=frame"))
        
    return StreamingHttpResponse(get_frame(i, ips[descricao]),content_type="multipart/x-mixed-replace;boundary=frame")


#     return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
def get_frame(self, ip):
    # cameras = Cameras.objects.get(pk=ip)
    count = 0
    center_points_prev_frame = []
    tracking_objects = {}
    track_id = 0

    print('ip no get frame:',ip)

    # camera = cv2.VideoCapture(0) 
    camera = cv2.VideoCapture(ip)
    # camera.open("http://192.168.0.100:8080/videofeed")

    try:
        while True:
            
            _, img = camera.read()
            img = cv2.resize(img, (280, 280)) 
            # count += 1
            # center_points_cur_frame = []
            
            # classes, scores, boxes = model.detect(img, 0.1, 0.2)

            # for (classid, score, box) in zip(classes, scores, boxes):
            #     (x,y,w,h) = box
            #     cx = int((x + x + w) /2)
            #     cy = int((y + y + h) /2)
            #     center_points_cur_frame.append((cx,cy))
                
            #     # cv2.circle(img, (cx, cy), 5, (0,0, 255), -1)
            #     cv2.rectangle(img, (x,y), (x + w, y+h), (0,255,0), 2)

            # if count <= 2:
            #     for pt in center_points_cur_frame:
            #         for pt2 in center_points_prev_frame:
            #             distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                        
            #             if distance < 20:
            #                 tracking_objects[track_id] = pt
            #                 track_id += 1
            # else:
            #     tracking_objects_copy = tracking_objects.copy()
            #     center_points_cur_frame_copy = center_points_cur_frame.copy()
                
            #     for object_id, pt2 in tracking_objects_copy.items():
            #         object_exists = False
            #         for pt in center_points_cur_frame_copy:
            #             distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                    
            #             if distance < 20:
            #                 tracking_objects[object_id] = pt
            #                 object_exists = True
            #                 if pt in center_points_cur_frame:
            #                     center_points_cur_frame.remove(pt)
            #                 continue

            #         if not object_exists:
            #             tracking_objects.pop(object_id)

            #     for pt in center_points_cur_frame:
            #         tracking_objects[track_id] = pt
            #         track_id += 1
            
            # for object_id, pt in tracking_objects.items():
            #     cv2.circle(img, pt, 5, (0,0, 255), -1)
            #     # cv2.putText(img, str(object_id),(pt[0], pt[1] - 7), 0, 1, (0, 0, 255), -2)
            #     # cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

            # center_points_prev_frame = center_points_cur_frame.copy()

            # print(tracking_objects)
            
            if cv2.waitKey(0) == 27:
                break
            
            imgencode=cv2.imencode('.jpg',img)[1]
            stringData=imgencode.tostring()
            yield((b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n'))
        del(camera)
    except: 
        pass

    
def indexscreen(request): 
    try:
        template = "templates/index.html"
        return render(request,template)
    except:
        print("error")

# Configuração cameras

def cameras(request):
    cameras = Cameras.objects.all()
    context ={
        'cameras': cameras,
    }

    return render(request, 'cameras/camera.html', context)

def configuracao(request):
    cameras = Cameras.objects.all()
    paginator = Paginator(cameras, 7)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    context ={
        'cameras': cameras,
        'page_obj':page_obj
    }
    return render(request, 'cameras/configuracao.html', context)

def novacamera(request):
    cameras = Cameras.objects.all()
    context = {
        'cameras': cameras,

    }
    if request.method == 'GET':
        return render(request, 'cameras/novacamera.html', context)

    if request.method == 'POST':
        ip = request.POST['ip']

        if not ip:
            return render(request, 'cameras/novacamera.html', context)
        
        descricao = request.POST['descricao']

        if not descricao:
            return render(request, 'cameras/novacamera.html', context)

        Cameras.objects.create( ip=ip,  descricao=descricao)        
        return redirect('configuracao/')


def deletarcamera(request, id):
    cameras = Cameras.objects.get(pk=id)
    cameras.delete()
    return redirect('configuracao/')


def editcamera(request, id):
    cameras = Cameras.objects.get(pk=id)
    context = {
        'cameras': cameras,
        'values': cameras,
        
    }
    if request.method == 'GET':
        return render(request, 'cameras/editcamera.html', context)

    if request.method == 'POST':
        ip = request.POST['ip']

        if not ip:
            return render(request, 'cameras/editcamera.html', context)

        descricao = request.POST['descricao']

        if not descricao:
            return render(request, 'cameras/editcamera.html', context)

        cameras.ip = ip
        cameras.descricao = descricao

        cameras.save()

        return redirect('configuracao/')
