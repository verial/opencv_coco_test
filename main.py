import os

import cv2
import cvzone
import serial
from flask import Flask, Response, render_template

from servo import move_camera_to_target

#НОМЕР COM ПОРТА
ser = serial.Serial('COM6', 1200)
ser.close()

IMAGE_CENTER = (320, 240)


app = Flask(__name__)
exiting = False
@app.route("/")
def index():
    return render_template("index.html")


def send_pelco_d_command(command):
    ser.open()
    ser.write(command)
    ser.close()

def center_finder(box):
    rectangle_center = (box[0] + box[2] // 2, box[1] + box[3] // 2)
    return rectangle_center


def gen():
    thres = 0.5
    nmsThres = 0.2
    cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)

    classNames = []
    classFile = "coco.names"
    with open(classFile, "rt") as f:
        classNames = f.read().split("\n")
    print(classNames)
    configPath = "model_mobilenet.pbtxt"
    weightsPath = "frozen_inference_graph.pb"

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    temp_command = None
    while True:
        success, img = cap.read()
        classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
        try:
            for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classNames[classId - 1] == "person":
                    target_center = center_finder(box)
                    target_center = target_center[0], target_center[1]                    # Calculate the difference between the target center and the image center
                    dx = target_center[0] - IMAGE_CENTER[0]
                    dy = target_center[1] - IMAGE_CENTER[1]
                    cvzone.cornerRect(img, box)
                    cv2.circle(img, target_center, 5, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                                (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (0, 255, 0), 2)
                    command = move_camera_to_target(dx, dy)
                    if temp_command != command:
                        temp_command = command
                        send_pelco_d_command(command)
        except:
            pass
        success, buffer = cv2.imencode(".jpg", img)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/exit")
def exit_app():
    global exiting
    exiting = True
    return "Done"


@app.teardown_request
def teardown(exception):
    if exiting:
        os._exit(0)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
