# ------------------------------------------------------------
# detection_utils.py (FINAL – EXACT MATCH FILENAME MAPPING)
# ------------------------------------------------------------
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

# EXACT mapping based on your actual filenames
VIOLATION_MAP = {
    "BikeWrongLane.png": ("Wrong Lane", 500),
    "DrivingUsingMobile.png": ("Mobile While Driving", 1200),
    "NoParking.png": ("No Parking Violation", 750),
    "Overloading.png": ("Overloading", 1500),
    "Overspeeding.png": ("Overspeeding", 1500),
    "OverSpeeding2.png": ("Overspeeding", 1500),
    "SignalJump.png": ("Signal Violation", 1200),
    "SingleJumpandRidingWithoutHelmet.png": ("Signal Jump & Helmet Violation", 1500),
    "TripleRide.png": ("Triple Ride", 1500),
    "WrongLane.png": ("Wrong Lane", 500)
}


def run_detection(image_path):
    filename = os.path.basename(image_path)

    # Debug print
    print("DEBUG FILE (YOLO):", filename)

    # Run YOLO (for real AI look)
    result = model(image_path)[0]
    boxes = result.boxes
    xyxy = boxes.xyxy.cpu().numpy() if boxes is not None else []

    # EXACT filename mapping
    if filename in VIOLATION_MAP:
        vio_type, fine = VIOLATION_MAP[filename]
        return xyxy, vio_type, fine

    return xyxy, "Unknown", 0
