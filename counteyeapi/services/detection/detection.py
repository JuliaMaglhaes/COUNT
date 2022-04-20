import cv2
import time
from cv2 import VideoCapture

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []

def detection_product(image):
    with open("names.names", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
    recebimento = cv2.imread(f"media\count\{image}")
    cap = cv2.cvtColor(recebimento, cv2.COLOR_BGR2GRAY)

    modelWeightsPath = "counteyeapi\services\detection\yolov3_training_last.weights"
    modelConfigurationPath = "counteyeapi\services\detection\yolov3_testing.cfg"

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