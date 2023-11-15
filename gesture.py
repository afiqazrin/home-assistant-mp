import cv2
import mediapipe as mp
import pyautogui
from subprocess import call, run

# subprocess required to adjust volume because if volume is initally muted, vokume change wont work
run(["pactl", "set-sink-mute", "0", "0"])
run(["pactl", "set-sink-volume", "0", "50%"])

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
                if id == 4:
                    cv2.circle(img = image, center = (x,y), radius = 8, color = (0, 0, 255), thickness= 3)
                    x2 = x
                    y2 = y
        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
        print(dist)
        cv2.line(image,(x1,y1),(x2,y2),(0,255, 0), 5)
        if dist > 50:
            call(["amixer", "-D", "pulse", "sset", "Master", str(dist)+"%"])
            valid = True

        else:
            call(["amixer", "-D", "pulse", "sset", "Master", str(dist)+"%"])
            valid = True

    # cv2.imshow("Test", image)

    # 10 ms delay before capturing next frame
    key = cv2.waitKey(10)
    # 27 is escape key, exits from the webcam
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()