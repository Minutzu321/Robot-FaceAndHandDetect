import socket
import numpy as np
import cv2
import struct
import time
import jpysocket
from PIL import Image
import io
import math

import mediapipe as mp
from numpy.lib.twodim_base import tri
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(("192.168.43.1",8091))


with mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:
    while True:
        time.sleep(0.0001)
        buf = b''
        while len(buf) < 4:
            buf += sock.recv(4 - len(buf))
        size = struct.unpack('!i', buf)[0]
        try:
            frame = sock.recv(size)
            array = np.frombuffer(frame, dtype='uint8')
            img = cv2.imdecode(array, 1)
        
            image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        except:
            continue
        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        best = None
        barie = 0
        if results.multi_hand_landmarks:
            for detection in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, detection, mp_hands.HAND_CONNECTIONS)
                deget_mare = detection.landmark[mp_hands.HandLandmark.THUMB_TIP]
                deget_mic = detection.landmark[mp_hands.HandLandmark.PINKY_TIP]
                distance = math.sqrt( ((deget_mare.x-deget_mic.x)**2)+((deget_mare.y-deget_mic.y)**2) )
                arie = int(distance*100)
                trimite = "persoana "+str(int(10*detection.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x))+"%"+str(int(10*detection.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y))+"%"+str(arie)+'\n'
                # print(trimite)
                    # print(10*detection.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, 10*detection.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                # print(type(trimite))
                sock.send(trimite.encode())
        cv2.imshow('RiverWolves detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
