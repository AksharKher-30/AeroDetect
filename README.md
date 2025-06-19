# Drone, Helicopter, and Aircraft Detection using YOLOv11n 🚁

This project demonstrates an end-to-end pipeline for detecting drones, helicopters, and airplanes in both images and videos using the YOLOv11n object detection model. It features a clean web interface built with FastAPI and allows users to upload multiple images or a video file, view previews, and see real-time predictions.

---

## 🌐 Project Overview

This repository provides a complete solution to:
- Detect drones, helicopters, and aircraft in both images and videos
- Use a custom-trained YOLOv11n object detection model
- Preview uploaded media and visualize detections on the web
- Run a FastAPI backend with a modern HTML/CSS/JS frontend
- Upload multiple images (batch detection) or a single video for processing
- Organize and serve predictions without saving unnecessary files permanently

--- 

## 📁 Project Structure

```bash
drone-detection-app/
├── app/
│   ├── main.py              # FastAPI app with endpoints
│   ├── model.py             # YOLOv11n model loading and prediction logic
│   ├── utils.py             # Utility functions (e.g., video processing)
│   ├── uploads/             # Temporary storage for uploaded files
│   └── output/              # Stores processed video results
│
├── static/
│   ├── web.css              # CSS styling for the web interface
│   └── web.js               # JS logic for uploading, previews, detection
│
├── templates/
│   └── web.html             # Jinja2 HTML template for the main UI
│
├── data/                    # YOLO formatted dataset
│   ├── images/
│   │   ├── train/ test/ val/
│   ├── labels/
│   │   ├── train/ test/ val/
│   └── dataset.yaml
│
├── csv_to_yolo.py           # Converts annotation CSV to YOLO format
├── drone_detection.ipynb    # Model training notebook
├── test.jpg                 # Example image
├── yolov11n.pt              # Trained YOLOv11n model weights
└── runs_n/, runs/           # YOLO training outputs (optional)
```

---

## ⚙️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/AksharKher-30/AeroDetect.git
cd drone-detection-app
```

2.  **Install Dependencies**

```bash
pip install -r requirements.txt
```
> Make sure you have Python 3.8+ and pip installed on your system.

3. Start the Web Server

```bash
uvicorn app.main:app --reload
```
> Visit: http://127.0.0.1:8000

--- 

## 📁 Data Preparation
- The dataset contains annotations in Pascal VOC (XML) format for drones, helicopters, and airplanes.
- To convert them into YOLO format, use the provided script:
  ```bash
  python csv_to_yolo.py
  ```
This script will:
- Parse all XML annotation files from the dataset
- Convert bounding box annotations to YOLO-compatible .txt format
- Automatically place the converted .txt files into the corresponding labels/ directoies.
  
Ensure your dataset is structured as follows before training:
```bash
data/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```
> ⚠️ Make sure the image and label filenames match exactly for YOLO training or you can change the path in the code if different names of files/folder.

The trained weights will be saved under:
```bash
Aero Detect/runs_n/drone_train_n/drone_detector_n/weights/best.pt
├── best.pt
└── last.pt
```
> **best.pt** is used for inference.

## 🧪 How to Use
After starting the webpage:

🌄 Image Prediction
-	Upload up to 8 images
-	Preview appears instantly
-	Click Detect to see prediction overlays

🎞️ Video Prediction
-	Upload one video (MP4 format recommended)
-	Preview shows the original video
-	Click Detect to view the result in-place

## 📊 Performance

Validation results on the test set using **YOLOv11n**  
Image size: `512`, Confidence threshold: `0.35`, IoU threshold: `0.5`

| Class        | Images | Instances | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|--------------|--------|-----------|-----------|--------|---------|--------------|
| **All**      | 603    | 497       | 0.920     | 0.928  | 0.936   | 0.592        |
| **Drone**    | 220    | 224       | 0.887     | 0.879  | 0.874   | 0.447        |
| **Helicopter** | 140  | 140       | 0.985     | 0.964  | 0.981   | 0.676        |
| **Airplane** | 133    | 133       | 0.887     | 0.940  | 0.952   | 0.655        |

---

## 🚀 Working Demo
<video width="100%" controls>
  <source src="assets/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
