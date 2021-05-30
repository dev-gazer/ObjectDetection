import cv2 as cv
import sys, os
from starman_jr import send_photo
from dotenv import load_dotenv
import time

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(1)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()

    def identify_camera(self):
        load_dotenv()
        telegram = os.getenv('telegram')
        classNames = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        #Custom config and weights path for the Mustang
        configpath = 'custom-yolov4-detector.cfg'
        weigthspath = 'custom-yolov4-detector_best.weights'

        net = cv.dnn_DetectionModel(weigthspath, configpath)
        net.setInputSize(320,320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        #Standard configs and weights path
        configpath2 = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weigthspath2 = 'frozen_inference_graph.pb'

        net2 = cv.dnn_DetectionModel(weigthspath2, configpath2)
        net2.setInputSize(320,320)
        net2.setInputScale(1.0 / 127.5)
        net2.setInputMean((127.5, 127.5, 127.5))
        net2.setInputSwapRB(True)

        self.video.set(3,640)
        self.video.set(4,480)
        success, img = self.video.read()
        count = 0
        classIds, confs, bbox = net.detect(img, confThreshold=0.5)
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv.rectangle(img, box, color=(0, 0, 255),thickness=2)
                cv.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                if classNames[classId-1] == 'mustang':
                    count += 1
                    print(f'Count {count}')
                    if count >= 4:
                        print('Found the Mustang')
                        cv.imwrite('temp/mustang.png', img)
                        send_photo('temp/mustang.png', 'Found the Mustang!', telegram)
                        os.remove('temp/mustang.png')
                        count = 0
                        time.sleep(15)
        
        classIds2, confs2, bbox2 = net2.detect(img, confThreshold=0.5)
        if len(classIds2) != 0:
            for classId2, confidence2, box2 in zip(classIds2.flatten(), confs2.flatten(), bbox2):
                cv.rectangle(img, box2, color=(0, 0, 255),thickness=2)
                cv.putText(img, classNames[classId2-1].upper(), (box2[0]+10, box2[1]+30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


        ret, jpeg = cv.imencode('.jpg', img)
        return jpeg.tobytes()
