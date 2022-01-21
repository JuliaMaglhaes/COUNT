import cv2

cam = cv2.VideoCapture(0)


while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        cv2.destroyAllWindows()

    cv2.imshow('Stream', frame)