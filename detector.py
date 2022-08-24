# Written by Sy

import cv2
import mediapipe as mp
import time
import math

def DrawPose(cap):
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    pose = mpPose.Pose()

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        
        lmlist = []
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id, cx, cy])
                cv2.circle(img, (cx, cy), 5, (0,255,0), cv2.FILLED)
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN,
        3, (255,0,0), 3)

        img = cv2.resize(img, (500,800))
        cv2.imshow("Image", img)
        cv2.waitKey(10)
        
cap = cv2.VideoCapture("Put Ur video here.mp4")
DrawPose(cap)
