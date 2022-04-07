import cv2
import time
from cv2 import VideoCapture

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]


with open(r"C:\Users\julia\OneDrive\Área de Trabalho\COUNT\counteyeapi\services\detection\names.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cap = cv2.VideoCapture()
cap.open("http://100.100.214.110:8080/videofeed")


modelWeightsPath = "counteyeapi\services\detection\yolov3_training_last.weights"
modelConfigurationPath = "counteyeapi\services\detection\yolov3_testing.cfg"

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
        label = f"{class_names[0]} : {score}"
        # trust = score[classid]

        # if conditional == True:
        #     # if trust >= threshold:
        #     counted_items = counted_items + 1
        #     conditional = False
            # print(score[classid])

        # print(counted_items)
        #print(class_names[classid[0]], counted_items)

        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow("Detector", frame)

    if cv2.waitKey(0) == 27:
        # tecla para sair
        break

cap.release()
cv2.destroyAllWindows()