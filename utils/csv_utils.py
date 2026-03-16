# ------------------------------------------------------------
# csv_utils.py (Final Stable Version)
# ------------------------------------------------------------

import os
import pandas as pd


# ------------------------------------------------------------
# CSV HEADER (MUST MATCH app.py EXACTLY)
# ------------------------------------------------------------
COLUMNS = [
    "vehicle_number",
    "vehicle_color",
    "violation",
    "fine_amount",
    "date_of_violation",
    "time_of_violation",
    "location",
    "status",
    "detection_confidence",
    "image_name"
]


# ------------------------------------------------------------
# CREATE CSV IF NOT EXISTS
# ------------------------------------------------------------
def ensure_csv(csv_path):
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(csv_path, index=False)
        print("[CSV] Created new CSV file:", csv_path)


# ------------------------------------------------------------
# LOAD CSV SAFELY
# ------------------------------------------------------------
def load_csv(csv_path):
    ensure_csv(csv_path)
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print("[CSV LOAD ERROR]:", e)
        return pd.DataFrame(columns=COLUMNS)


# ------------------------------------------------------------
# APPEND A NEW ROW TO CSV
# ------------------------------------------------------------
def append_violation_row(csv_path, plate, color, violation, fine, date, time, location,
                         status, confidence, image_name, email=""):
    """
    Appends a row and returns the index of the new row.
    """

    ensure_csv(csv_path)

    df = load_csv(csv_path)

    new_row = {
        "vehicle_number": plate if plate else "UNKNOWN",
        "vehicle_color": color,
        "violation": violation,
        "fine_amount": fine,
        "date_of_violation": date,
        "time_of_violation": time,
        "location": location,
        "status": status,
        "detection_confidence": round(float(confidence), 3),
        "image_name": image_name,
        "email": email
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(csv_path, index=False)

    new_index = len(df) - 1
    print(f"[CSV] Added row at index {new_index}")

    return new_index
