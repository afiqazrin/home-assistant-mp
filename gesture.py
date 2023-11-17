import cv2
import mediapipe as mp
import pyautogui
import subprocess
from subprocess import call, run

# subprocess required to adjust volume because if volume is initally muted, volume change wont work
call(["pactl", "set-sink-mute", "0", "0"])
call(["amixer", "-D", "pulse", "sset", "Master", "50%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
hands = mp.solutions.mediapipe.solutions.hands.Hands()
drawing_utils = mp.solutions.mediapipe.solutions.drawing_utils


while True:
    # capture image from webcam
    _, image = webcam.read()
    frame_height, frame_width, _ = image.shape
    # convert BGR image to RGB image
    formatted_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = hands.process(formatted_image)
    # detect all fingers
    fingers = output.multi_hand_landmarks
    if fingers:
        for finger in fingers:
            drawing_utils.draw_landmarks(image, finger)
            fingerpoints = finger.landmark
            # collecting all fingerpoints
            for id, fingerpoint in enumerate(fingerpoints):
                x = int(fingerpoint.x * frame_width)
                y = int(fingerpoint.y * frame_height)
                # ids for each finger can be found by searching up mediapipe hands diagram on google.
                # in this case, 8 is index finger tip and 4 is the thumb
                if id == 8:
                    cv2.circle(img = image, center = (x,y), radius = 8, color = (0, 255, 255), thickness = 3)
                    x1 = x
                    y1 = y
                    # print(y1)
                if id == 4:
                    cv2.circle(img = image, center = (x,y), radius = 8, color = (0, 0, 255), thickness= 3)
                    x2 = x
                    y2 = y
        x_dist = abs(x2 - x1)
        y_dist = abs(y2 - y1)
        if x_dist == 0:
            x_dist = 1
        if x_dist > y_dist:
            call(["sudo", "brightnessctl", "-d", "intel_backlight", "s", str(x_dist) + "%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Horizontal hand")
        # Add your code for horizontal hand here
        else:
            call(["amixer", "-D", "pulse", "sset", "Master", str(y_dist)+"%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Vertical hand")
        # Add your code for vertical hand here
        print("X: ",  x_dist)
        print("Y: ", y_dist)
        cv2.line(image,(x1,y1),(x2,y2),(0,255, 0), 5)

    cv2.imshow("Test", image)

    # 10 ms delay before capturing next frame
    key = cv2.waitKey(10)
    # 27 is escape key, exits from the webcam
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()