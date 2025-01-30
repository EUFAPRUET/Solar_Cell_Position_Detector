import cv2
from ultralytics import YOLO

model = YOLO("SunDetectionModel.pt")

res = model(source=0, show=True, conf=0.4,save=True)

while True:
    if cv2.waitKey(1) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()