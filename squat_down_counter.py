# Written by Sy in Jan 2023

import cv2
import mediapipe as mp
import time
import math

def findAngle(cap, p1, p2, p3):
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    count = 0
    condition = 0
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
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id, cx, cy])
        
        x1, y1 = lmlist[p1][1:]
        x2, y2 = lmlist[p2][1:]
        x3, y3 = lmlist[p3][1:]
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 15, (0,255,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0,255,0), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (0,255,0), cv2.FILLED)

        #Calculate the angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        print(angle)
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
        cv2.putText(img, str(int(angle)), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 5)
        
        #calculate how many time squat
        if angle >170:
            condition = "stand"
        if angle < 83 and condition == "stand":
            condition = "sit"
            count += 1
        cv2.putText(img, str(count), (600,50),cv2.FONT_HERSHEY_PLAIN, 4, (0,255,0), 4)


        img = cv2.resize(img, (400,700))
        cv2.imshow("Image", img)
        cv2.waitKey(10)
       
        

video = cv2.VideoCapture("xxx.mp4")
findAngle(video, 23, 25, 27)
