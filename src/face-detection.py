import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

fps=0
LED_PIN = 17

def visualize_fps(image, fps: int):
    if len(np.shape(image)) < 3:
        text_color = (255, 255, 255)  # white
    else:
        text_color = (0, 255, 0)  # green
    row_size = 20  # pixels
    left_margin = 24  # pixels

    font_size = 1
    font_thickness = 1

    # Draw the FPS counter
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    return image


# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)


while True:
    # ----------------------------------------------------------------------
    # record start time
    GPIO.setmode(GPIO.OUT)
    GPIO.setup(LED_PIN, GPIO.OUT)
    start_time = time.time()
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len((faces)) > 0:
      GPIO.output(LED_PIN, GPIO.HIGH)
    else:
      GPIO.output(LED_PIN, GPIO.LOW)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display
    cv2.imshow('img', visualize_fps(img, fps))
    # ----------------------------------------------------------------------
    # record end time
    end_time = time.time()
    # calculate FPS
    seconds = end_time - start_time
    fps = 1.0 / seconds
    print("Estimated fps:{0:0.1f}".format(fps))
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()