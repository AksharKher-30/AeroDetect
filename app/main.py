from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import cv2
import base64
import numpy as np
import io
from typing import List
from app.model import detect_drones

# Create necessary directories
os.makedirs("app/uploads", exist_ok=True)
os.makedirs("app/output", exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="app/output"), name="output")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})


@app.post("/predict/images/")
async def predict_multiple_images(files: List[UploadFile] = File(...)):
    try:
        if len(files) > 8:
            return JSONResponse(status_code=400, content={"error": "Maximum 8 images allowed."})

        result_images = []

        for file in files:
            contents = await file.read()
            np_arr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if image is None:
                continue

            result_img = detect_drones(image)

            _, buffer = cv2.imencode('.jpg', result_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            result_images.append(f"data:image/jpeg;base64,{img_base64}")

        if not result_images:
            return JSONResponse(status_code=400, content={"error": "No valid images found."})

        return JSONResponse(content={"result_images": result_images})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Batch prediction failed: {str(e)}"})


@app.post("/predict/video/")
async def predict_video(video: UploadFile = File(...)):
    try:
        base_name, ext = os.path.splitext(video.filename)
        input_path = f"app/uploads/{video.filename}"
        output_filename = f"{base_name}_output{ext}"
        output_path = f"app/output/{output_filename}"

        with open(input_path, "wb") as f:
            f.write(await video.read())

        process_video_with_yolo(input_path, output_path)

        return JSONResponse(content={"video_url": f"/output/{output_filename}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


def process_video_with_yolo(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video file")

    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = detect_drones_on_frame(frame)
        out.write(processed_frame)

    cap.release()
    out.release()


def detect_drones_on_frame(frame):
    return detect_drones(frame)  # Call your actual YOLO detection function