import socket
import numpy as np
import cv2
import struct
import time
import jpysocket
from PIL import Image
import io

import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(("192.168.43.1",8091))

faceCascade = cv2.CascadeClassifier("hc.xml")


with mp_face_detection.FaceDetection(
    min_detection_confidence=0.6) as face_detection:
    while True:
        time.sleep(0.015)
        buf = b''
        while len(buf) < 4:
            buf += sock.recv(4 - len(buf))
        size = struct.unpack('!i', buf)[0]
        try:
            frame = sock.recv(size)
            array = np.frombuffer(frame, dtype='uint8')
            img = cv2.imdecode(array, 1)
            image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            image.flags.writeable = False
            results = face_detection.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            best = None
            barie = 0
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
                    location_data = detection.location_data
                    x = [keypoint.x for keypoint in location_data.relative_keypoints]
                    y = [keypoint.y for keypoint in location_data.relative_keypoints]

                    c1x, c1y = min(x), min(y)
                    c2x, c2y = max(x), max(y)

                    bl, bL = abs(c2x-c1x), abs(c2y-c1y)
                    arie = int(bl*bL*1000)
                    if arie > barie:
                        barie = arie
                        best = ("persoana "+str(int(10*mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).x))+"%"+str(int(10*mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).y))+"%"+str(arie)+'\n').encode()
            if barie != 0:
                sock.send(best)
            cv2.imshow('RiverWolves detection', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        except Exception as ex: print(ex)
