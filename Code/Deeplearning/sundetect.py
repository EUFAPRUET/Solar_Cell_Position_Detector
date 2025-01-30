import cv2
from ultralytics import YOLO
import time

model = YOLO("SunDetectionModel.pt")

cap = cv2.VideoCapture(0)

width = 640
height = 480
center_x_img = width // 2
center_y_img = height // 2

pan_angle = 90
tilt_angle = 90

Kx = 0.01
Ky = 0.01

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, conf=0.5)
    boxes = results[0].boxes
    
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if cls_id == 0:
            x1, y1, x2, y2 = box.xyxy[0]

            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)

            offset_x = x_center - center_x_img
            offset_y = y_center - center_y_img

            pan_angle -= offset_x * Kx
            tilt_angle += offset_y * Ky

            if pan_angle > 180: 
                pan_angle = 180
            if pan_angle < 0:   
                pan_angle = 0
            if tilt_angle > 180: 
                tilt_angle = 180
            if tilt_angle < 0:   
                tilt_angle = 0
            
            conf_percent = conf * 100
            
            text_info = (f"Center=({int(x_center)}, {int(y_center)}) "
                         f"Pan={pan_angle:.1f} Tilt={tilt_angle:.1f} "
                         f"Conf={conf_percent:.1f}%")
            cv2.putText(frame, text_info, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow("Simulation", frame)
    
    if cv2.waitKey(1) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()
