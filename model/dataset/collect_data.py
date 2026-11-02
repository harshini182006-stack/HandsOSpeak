import cv2
from pathlib import Path
from datetime import datetime

# Dataset location
DATASET_PATH = Path(__file__).parent / "dataset" / "raw"

# Enter the name of the sign
label = input("Enter sign name (example: hello): ").strip().lower()

if not label:
    print("Please enter a sign name.")
    exit()

# Create a folder for this sign
save_folder = DATASET_PATH / label
save_folder.mkdir(parents=True, exist_ok=True)

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("Camera ready!")
print("Press R to record a 3-second sample.")
print("Press Q to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read camera.")
        break

    cv2.imshow("Hands O Speak - Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('r'):
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4"
        filepath = save_folder / filename

        height, width = frame.shape[:2]
        writer = cv2.VideoWriter(
            str(filepath),
            cv2.VideoWriter_fourcc(*"mp4v"),
            20,
            (width, height)
        )

        print("Recording for 3 seconds...")

        for _ in range(60):
            success, frame = camera.read()

            if not success:
                break

            writer.write(frame)
            cv2.imshow("Hands O Speak - Data Collection", frame)
            cv2.waitKey(1)

        writer.release()
        print("Sample saved:", filepath)

camera.release()
cv2.destroyAllWindows()