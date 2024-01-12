import mediapipe as mp
import cv2
import pyautogui
import subprocess
from subprocess import call
from projectdb import insertnowtime, is_table_empty, cleanOldEntries, selectNewestTime, find_emergency_contact
import queue
import threading
from datetime import datetime
import time
from whatsapp import send_message
from texttospeech import speak
from picamera2 import Picamera2
from bulb import setBulbBrightness, turnOnLightBulb, turnOffLightBulb
bulbThread = None

def bulb_thread_function(y_dist):
    print("Thread started: ", y_dist)
    setBulbBrightness(y_dist)
def process_frame(frame_type):
    piCam = Picamera2()
    piCam.preview_configuration.main.size=(320,240)
    piCam.preview_configuration.main.format="RGB888"
    piCam.preview_configuration.align()
    piCam.configure("preview")
    piCam.start()
    global bulbThread
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    hands = mp.solutions.mediapipe.solutions.hands.Hands()
    drawing_utils = mp.solutions.mediapipe.solutions.drawing_utils
    x1 = y1 = x2 = y2 = 0
    count = 0
    while True:
        frame=piCam.capture_array()
        if frame_type == "system_control":
            frame_height, frame_width, _ = frame.shape
            # convert BGR image to RGB image
            formatted_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = hands.process(formatted_image)
            # detect all fingers
            fingers = output.multi_hand_landmarks
            if fingers:
                for finger in fingers:
                    drawing_utils.draw_landmarks(frame, finger)
                    fingerpoints = finger.landmark
                    # collecting all fingerpoints
                    for id, fingerpoint in enumerate(fingerpoints):
                        x = int(fingerpoint.x * frame_width)
                        y = int(fingerpoint.y * frame_height)
                        # ids for each finger can be found by searching up mediapipe hands diagram on google.
                        # in this case, 8 is index finger tip and 4 is the thumb
                        if id == 8:
                            cv2.circle(
                                img=frame,
                                center=(x, y),
                                radius=8,
                                color=(0, 255, 255),
                                thickness=3,
                            )
                            x1 = x
                            y1 = y
                            # print(y1)
                        if id == 4:
                            cv2.circle(
                                img=frame,
                                center=(x, y),
                                radius=8,
                                color=(0, 0, 255),
                                thickness=3,
                            )
                            x2 = x
                            y2 = y
                x_dist = abs(x2 - x1)
                y_dist = abs(y2 - y1)
                if x_dist == 0:
                    x_dist = 1
                if x_dist > y_dist:
                    # call(
                    #     [
                    #         "sudo",
                    #         "brightnessctl",
                    #         "-d",
                    #         "intel_backlight",
                    #         "s",
                    #         str(x_dist) + "%",
                    #     ],
                    #     stdout=subprocess.DEVNULL,
                    #     stderr=subprocess.DEVNULL,
                    # )
                    # print("Horizontal hand")
                    print()
                # Add your code for horizontal hand here
                else:
                    call(
                        ["amixer", "-D", "pulse", "sset", "Master", str(y_dist) + "%"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    print("Vertical hand")
                # Add your code for vertical hand here
                print("X: ", x_dist)
                print("Y: ", y_dist)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv2.imshow("Systems Control", frame)
            pass
        elif frame_type == "person_detection":
            if is_table_empty():
                # print("table_empty")
                insertnowtime()
            else:
                # print("not_table_empty")
                pass
            output = selectNewestTime()
            # print("All the data")
            for row in output:
                timepast = row[0]
                cleanOldEntries(timepast)

            timepast2 = timepast

            now = datetime.now()

            now1 = str(now)
            now2 = datetime.strptime(now1, "%Y-%m-%d %H:%M:%S.%f")

            lasttime = datetime.strptime(timepast2, "%Y-%m-%d %H:%M:%S.%f")

            # calculating time diff
            timediff = now2 - lasttime
            timedelta = timediff.total_seconds()
            timediffmin = timedelta / 60
            # print(str(timediffmin))
            # alarm for time
            if timediffmin > 0.5:
                # insert system will say alarm
                insertnowtime()
                count += 1
                print(count)
                speak("Please make yourself visible infront of the camera")
                if count == 3:
                    send_message(find_emergency_contact(), f"Person is not detected by camera as of {now1}")
                    # insert text
                    count = 0
            fg_mask = bg_subtractor.apply(frame)

            # Apply some morphological operations to reduce noise
            fg_mask = cv2.erode(fg_mask, None, iterations=2)
            fg_mask = cv2.dilate(fg_mask, None, iterations=2)

            # Find contours in the foreground mask
            contours, _ = cv2.findContours(
                fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                if cv2.contourArea(contour) > 1000:  # Adjust this threshold as needed
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(
                        frame, (x, y), (x + w, y + h), (0, 255, 0), 2
                    )  # drawing rectangle on movement object
                    insertnowtime()
                    
                    count = 0
            cv2.imshow("Person Detection", frame)
            pass
        elif frame_type == "bulb_control": 
                frame_height, frame_width, _ = frame.shape
                # convert BGR image to RGB image
                formatted_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                output = hands.process(formatted_image)
                # detect all fingers
                fingers = output.multi_hand_landmarks
                if fingers:
                    for finger in fingers:
                        drawing_utils.draw_landmarks(frame, finger)
                        fingerpoints = finger.landmark
                        # collecting all fingerpoints
                        for id, fingerpoint in enumerate(fingerpoints):
                            x = int(fingerpoint.x * frame_width)
                            y = int(fingerpoint.y * frame_height)
                            # ids for each finger can be found by searching up mediapipe hands diagram on google.
                            # in this case, 8 is index finger tip and 4 is the thumb
                            if id == 8:
                                cv2.circle(
                                    img=frame,
                                    center=(x, y),
                                    radius=8,
                                    color=(0, 255, 255),
                                    thickness=3,
                                )
                                x1 = x
                                y1 = y
                                # print(y1)
                            if id == 4:
                                cv2.circle(
                                    img=frame,
                                    center=(x, y),
                                    radius=8,
                                    color=(0, 0, 255),
                                    thickness=3,
                                )
                                x2 = x
                                y2 = y
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                    y_dist = round(abs(y2 - y1) / 3, 0)
                    if y_dist < 12:
                        y_dist = 0
                    if y_dist >100:
                        y_dist = 100
                    if bulbThread is None or not bulbThread.is_alive():
                        bulbThread = threading.Thread(target=bulb_thread_function, args=(y_dist,))
                        bulbThread.start()
                        # time.sleep(5)
                    # Create and start the thread
                cv2.imshow("Light Bulb Control", frame)
        # Display the processed frame
        # 10 ms delay before capturing next frame
        key = cv2.waitKey(10)
        # 27 is escape key, exits from the webcam
        if key == 27:
            break
    cv2.destroyAllWindows()
