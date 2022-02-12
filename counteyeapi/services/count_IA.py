import cv2
import numpy as np
import matplotlib.pyplot as plt


def count_product(image_path):
    image = cv2.imread(f"media\count\{image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #plt.imshow(gray, cmap = 'gray')
    blur = cv2.GaussianBlur(gray, (1,1), 0)
    #plt.imshow(blur, cmap = 'gray')

    canny = cv2.Canny(blur, 1, 250, 3)
    dilated = cv2.dilate(canny, (1,1), iterations = 2)

    (cnt, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (0,255,0),2)
    return len(cnt)