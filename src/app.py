from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2 as cv

#to run on docker, type sudo docker run -it -p 5000:5000 --device /dev/video0 camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    #camera.identify_camera()
    while True:
        frame = camera.identify_camera()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)