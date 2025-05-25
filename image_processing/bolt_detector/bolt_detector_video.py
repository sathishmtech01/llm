from ultralytics import YOLO
import cv2

# Load your trained model
model = YOLO("runs/detect/train4/weights/best.pt")  # or path to your bolt model

# Open the video
video_path = "bolt-detection.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties for saving (optional)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# (Optional) Save output video with detections
out = cv2.VideoWriter('out-bolt-detection.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

bolt_index = [k for k, v in model.names.items() if v == "bolt"][0]  # Get class index of 'bolt'

frame_num = 0
bolt_found = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_num += 1

    # Run inference
    results = model(frame)[0]

    # Check if 'bolt' is detected
    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id == bolt_index:
            bolt_found = True
            print(f"[Frame {frame_num}] Bolt detected!")

    # Draw and save results (optional)
    annotated_frame = results.plot()
    out.write(annotated_frame)

cap.release()
out.release()

if bolt_found:
    print("\n✅ Bolt detected in video.")
else:
    print("\n❌ No bolt detected.")
