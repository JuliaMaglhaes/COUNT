import cv2
import time
from cv2 import VideoCapture

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
counted_items = 0
threshold = 0.3 
conditional = True

# limite para um carro ser contato

with open(r"C:\Users\julia\OneDrive\Área de Trabalho\AMBEV\OPENCV\coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cap = cv2.VideoCapture(0)

modelWeightsPath = "yolov3-tiny.weights"
modelConfigurationPath = "yolov3-tiny.cfg"

net = cv2.dnn.readNet(modelConfigurationPath, modelWeightsPath)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size = (416, 416), scale=1/255)

def readItem():
    print("eae")

while True:
    _, frame = cap.read()
    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = f"{class_names[classid[0]]} : {score}"
        # trust = score[classid]

        if conditional == True:
            # if trust >= threshold:
            counted_items = counted_items + 1
            conditional = False
            # print(score[classid])

        # print(counted_items)
        print(class_names[classid[0]], counted_items)

        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow("Detector", frame)

    if cv2.waitKey(1) == 27:
        # tecla para sair
        break

cap.release()
cv2.destroyAllWindows()