import cv2
import time
from cv2 import VideoCapture

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = [c.strip() for c in open('./counteyeapi/services/detection/names.names').readlines()]


cap = cv2.VideoCapture(0)
# cap.open(0)


modelWeightsPath = "counteyeapi\services\detection\yolov3_training_last.weights"
modelConfigurationPath = "counteyeapi\services\detection\yolov3_testing.cfg"

net = cv2.dnn.readNet(modelConfigurationPath, modelWeightsPath)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size = (416, 416), scale=1/255)

while True:
    _, frame = cap.read()
    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]
        label = f"{class_names[0]} : {score}"

        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imshow("Detector", frame)

    if cv2.waitKey(0) == 27:
        # tecla para sair
        break

cap.release()
cv2.destroyAllWindows()