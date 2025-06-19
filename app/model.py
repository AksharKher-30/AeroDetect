from ultralytics import YOLO
import numpy as np
import cv2

# Load the model once
model = YOLO('/Users/akshar/Documents/DL/Aero Detect/runs_n/drone_train_n/drone_detector_n/weights/best.pt')  # Update the path if needed

def detect_drones(image):
    # Convert OpenCV image (BGR) to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run prediction
    results = model.predict(source=rgb_image, save=False, verbose=False)

    # Get the result image with bounding boxes
    result_img = results[0].plot()  # result[0] contains one image’s prediction

    # Convert back to BGR for OpenCV compatibility
    result_img_bgr = cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR)
    return result_img_bgr