from ultralytics import YOLO
import os

# Load your trained YOLOv8 model
model = YOLO("runs/detect/train2/weights/best.pt")  # or "yolov8n.pt" if you want to test

# Path to the image you want to test
image_path = "dataset/images/train1/bolt_1.jpeg"  # replace with your image


# Run inference
results = model(image_path)
# print(results)
# Check if any object is detected (class 0 = bolt)
detected = False
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    print(cls_id)
    if cls_id == 0:  # '0' is the class index for 'bolt'
        detected = True
        break

# Output result
if detected:
    print(f"{image_path}: bolt")
else:
    print(f"{image_path}: other")
