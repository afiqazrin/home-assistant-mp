import cv2
import mediapipe as mp
import pyautogui
import subprocess
from subprocess import call
import threading
import queue
def capture_frames(webcam, frame_queue, stop_event):
    while not stop_event.is_set():
        _, frame = webcam.read()
        if frame is not None:
            frame_queue.put(frame)

def process_frames(frame_queue, stop_event):
    hands = mp.solutions.mediapipe.solutions.hands.Hands()
    drawing_utils = mp.solutions.mediapipe.solutions.drawing_utils

    x1 = y1 = x2 = y2 = 0

    while not stop_event.is_set():
        if not frame_queue.empty():
            frame = frame_queue.get()

            frame_height, frame_width, _ = frame.shape
            formatted_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = hands.process(formatted_image)
            fingers = output.multi_hand_landmarks

            if fingers:
                for finger in fingers:
                    drawing_utils.draw_landmarks(frame, finger)
                    fingerpoints = finger.landmark
                    for id, fingerpoint in enumerate(fingerpoints):
                        x = int(fingerpoint.x * frame_width)
                        y = int(fingerpoint.y * frame_height)
                        if id == 8:
                            cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                            x1 = x
                            y1 = y
                        if id == 4:
                            cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                            x2 = x
                            y2 = y
                x_dist = abs(x2 - x1)
                y_dist = abs(y2 - y1)
                if x_dist == 0:
                    x_dist = 1
                if x_dist > y_dist:
                    call(["sudo", "brightnessctl", "-d", "intel_backlight", "s", str(x_dist) + "%"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    call(["amixer", "-D", "pulse", "sset", "Master", str(y_dist) + "%"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

            cv2.imshow("Test", frame)
            key = cv2.waitKey(10)
            if key == 27:
                stop_event.set()

    cv2.destroyAllWindows()

def main_opencv():
    webcam = cv2.VideoCapture(0)
    frame_queue = queue.Queue()
    stop_event = threading.Event()

    capture_thread = threading.Thread(target=capture_frames, args=(webcam, frame_queue, stop_event))
    process_thread = threading.Thread(target=process_frames, args=(frame_queue, stop_event))

    capture_thread.start()
    process_thread.start()

    capture_thread.join()
    process_thread.join()

    webcam.release()


gesture_thread = threading.Thread(target=main_opencv)
gesture_thread.start()