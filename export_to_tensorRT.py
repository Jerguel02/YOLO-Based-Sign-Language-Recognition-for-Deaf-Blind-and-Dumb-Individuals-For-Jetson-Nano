from ultralytics import YOLO

# Load your YOLO model
model = YOLO('YOLOv8Checkpoint/YOLOv8Checkpoint/train4/weights/best.pt')

# Export to TensorRT format
model.export(format='engine')

