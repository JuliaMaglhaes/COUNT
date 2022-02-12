import cv2
import time
from cv2 import VideoCapture

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
counted_items = 0
threshold = 0.3 
conditional = True

# limite para um carro ser contato

def detection_product(image):
    with open("names.names", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
    cap = cv2.imread(f"media\count\{image}")
    modelWeightsPath = "yolov3_training_last.weights"
    modelConfigurationPath = "yolov3_testing.cfg"

    net = cv2.dnn.readNet(modelConfigurationPath, modelWeightsPath)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size = (416, 416), scale=1/255)

   
    predict = {
        "class": "Desconhecido"
    }
    try:
        classes, scores, boxes = model.detect(cap, 0.1, 0.2)
        for (classid, score, box) in zip(classes, scores, boxes):
            predict = {
                "class": class_names[0],
                "accuracy": score
            }
    except Exception as ex:
        pass

    return predict