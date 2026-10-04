import cv2
import numpy as np
import math
import pyautogui

from hand_tracking import HandDetector

# Webcam size
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector()

prevVol = 0

while True:

    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Index finger tip
        x2, y2 = lmList[8][1], lmList[8][2]

        # Center point
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles
        cv2.circle(img, (x1, y1), 10,
                   (255, 0, 255), cv2.FILLED)

        cv2.circle(img, (x2, y2), 10,
                   (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2),
                 (255, 0, 255), 3)

        cv2.circle(img, (cx, cy), 10,
                   (0, 0, 255), cv2.FILLED)

        # Distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert to percentage
        volPer = np.interp(length,
                           [30, 200],
                           [0, 100])

        volBar = np.interp(length,
                           [30, 200],
                           [400, 150])

        # Actual volume control
        if volPer > prevVol + 5:
            pyautogui.press("volumeup")
            prevVol = volPer

        elif volPer < prevVol - 5:
            pyautogui.press("volumedown")
            prevVol = volPer

        # Volume bar
        cv2.rectangle(img,
                      (50, 150),
                      (85, 400),
                      (0, 255, 0), 3)

        cv2.rectangle(img,
                      (50, int(volBar)),
                      (85, 400),
                      (0, 255, 0),
                      cv2.FILLED)

        # Percentage text
        cv2.putText(img,
                    f'{int(volPer)} %',
                    (40, 450),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 0, 0),
                    3)

    cv2.imshow("Hand Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()