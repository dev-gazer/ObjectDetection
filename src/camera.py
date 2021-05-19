import cv2 as cv

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()

    def identify_camera(self):
        #cap = self.video.read() #cv.VideoCapture(0)
        #cap.set(3,640)
        #cap.set(4,480)
        classNames = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weigthspath = 'frozen_inference_graph.pb'

        net = cv.dnn_DetectionModel(weigthspath, configpath)
        net.setInputSize(320,320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

       # while True:
        self.video.set(3,640)
        self.video.set(4,480)
        success, img = self.video.read()
        #img = cv.flip(img,1)
        #img.set(3,640)
        #img.set(4,480)
        classIds, confs, bbox = net.detect(img, confThreshold=0.5)
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv.rectangle(img, box, color=(0, 0, 255),thickness=2)
                cv.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        #cv.imshow('Output', img)
        #cv.waitKey(1)
        
        ret, jpeg = cv.imencode('.jpg', img)
        return jpeg.tobytes()
        #return