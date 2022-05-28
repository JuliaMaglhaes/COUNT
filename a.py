import os
from core.settings import BASE_DIR


modelWeightsPath = os.path.join(BASE_DIR, 'services\detection\yolov3_training_last.weights')
print(modelWeightsPath)