
import cv2
import mediapipe as mp
import csv
from pathlib import Path

# Folder locations
MODEL_PATH = Path(__file__).parent / "assets" / "hand_landmarker.task"
RAW_PATH = Path(__file__).parent / "dataset" / "raw"
OUTPUT_PATH = Path(__file__).parent / "dataset" / "processed" / "landmarks.csv"

# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=RunningMode.IMAGE,
    num_hands=2
)

# CSV columns
columns = ["label", "video", "frame", "handedness"]

for i in range(21):
    columns.extend([f"x{i}", f"y{i}", f"z{i}"])

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

all_rows = []

with HandLandmarker.create_from_options(options) as landmarker:

    for label_folder in RAW_PATH.iterdir():

        if not label_folder.is_dir():
            continue

        label = label_folder.name
        print("Processing sign:", label)

        for video_path in label_folder.iterdir():

            if video_path.suffix.lower() not in [".mp4", ".mov", ".avi"]:
                continue

            camera = cv2.VideoCapture(str(video_path))
            frame_number = 0

            while camera.isOpened():

                success, frame = camera.read()

                if not success:
                    break

                rgb_frame = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame
                )

                result = landmarker.detect(image)

                for hand_index, hand in enumerate(result.hand_landmarks):

                    handedness = "unknown"

                    if result.handedness and hand_index < len(result.handedness):
                        handedness = result.handedness[hand_index][0].category_name

                    row = {
                        "label": label,
                        "video": video_path.name,
                        "frame": frame_number,
                        "handedness": handedness
                    }

                    for i, point in enumerate(hand):
                        row[f"x{i}"] = point.x
                        row[f"y{i}"] = point.y
                        row[f"z{i}"] = point.z

                    all_rows.append(row)

                frame_number += 1

            camera.release()

            print("Processed:", video_path.name)

# Save extracted landmarks
with open(OUTPUT_PATH, "w", newline="") as file:

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(all_rows)

print("Extraction complete!")
print("Total hand samples:", len(all_rows))
print("Saved at:", OUTPUT_PATH)
