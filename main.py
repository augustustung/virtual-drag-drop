import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# example hand tracking: https://github.com/cvzone/cvzone/blob/master/Examples/HandTrackingExample.py

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(10, 100) # set thelight
handDetector = HandDetector(detectionCon=0.8)

class DragRect():
    def __init__(self, posCenter, size = [200, 200], color = (0, 0, 255)):
        self.posCenter = posCenter
        self.size = size
        self.color = color

    def update(self, newCursor):
        cx, cy = self.posCenter
        w, h = self.size
        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = newCursor # update position following cursor
            self.color = (255, 255, 0)
        else:
            self.color = (0, 0, 255)

rectList = []
for x in range(1):
    rectList.append(DragRect([x*250+150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # camera khong bi nguoc
    # hands, img = handDetector.findHands(img)  # with draw
    hands = handDetector.findHands(img, draw=False)  # without draw
    if hands:
        lmList = hands[0]["lmList"] # list array fingers
        # find distance between 2 fingers
        # ngon giua va ngon tro
        # length, _, _ = handDetector.findDistance(lmList[8], lmList[12], img)  # with draw
        length, _ = handDetector.findDistance(lmList[8], lmList[12])  # with draw

        cursor = lmList[8]  # ngon giua
        if length < 50:  # check if 2 fingers are not far away from them => click
            colorR = (0, 255, 255)
            # call the upadate here
            for rect in rectList:
                rect.update(cursor)

        ## Draw solid
        # for rect in rectList:
        #     cx, cy = rect.posCenter
        #     w, h = rect.size
        #     color = rect.color
        #     cv2.rectangle(img, (cx - w // 2, cy - h // 2),
        #                   (cx + w // 2, cy + h // 2), color, cv2.FILLED)
        #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

        ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        color = rect.color
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), color, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break