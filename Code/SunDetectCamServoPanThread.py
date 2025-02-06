import cv2
from ultralytics import YOLO
import time
import RPi.GPIO as GPIO

# กำหนดขา GPIO สำหรับ Servo Motor แกน X
PAN_SERVO_PIN = 18

# ตั้งค่า GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PAN_SERVO_PIN, GPIO.OUT)

# สร้าง PWM สำหรับ Servo
pan_servo = GPIO.PWM(PAN_SERVO_PIN, 50)
pan_servo.start(7.5)

# โหลดโมเดล YOLO
model = YOLO("SunDetectionModel.pt")

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# ขนาดภาพและจุดกึ่งกลาง
width = 640
center_x_img = width // 2

# Deadzone
deadzone_threshold = 10  # ลดค่า Deadzone เพื่อให้ดวงอาทิตย์อยู่ตรงกลางกล้องมากขึ้น

# ตั้งค่าเริ่มต้นให้ pan_angle
pan_angle = 60  # สำหรับ Servo NDS3115Mg, เริ่มต้นที่ 60 องศา (ตำแหน่งกึ่งกลางใหม่)

def map_angle(old_angle, old_min=0, old_max=180, new_min=0, new_max=120):
    """
    แปลงมุมจากช่วงเดิม (0-180°) เป็นช่วงใหม่ (0-120°) สำหรับ Servo NDS3115Mg
    """
    return new_min + (old_angle - old_min) * (new_max - new_min) / (old_max - old_min)

def angle_to_duty_cycle(angle):
    """
    แปลงมุม (0-120°) เป็น duty cycle (2.5% ถึง 12.5%) สำหรับ Servo NDS3115Mg
    """
    return 2.5 + (angle / 120.0) * 10

try:
    last_detected = False
    last_detection_time = time.time()
    detection_interval = 1  # ตรวจจับทุก 1 วินาที
    current_pan_angle = 60  # ตำแหน่งเริ่มต้นของ Servo

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_detection_time >= detection_interval:
            results = model.predict(frame, conf=0.5)
            boxes = results[0].boxes
            last_detection_time = current_time
        else:
            boxes = []

        if len(boxes) == 0:
            if last_detected:
                pan_servo.ChangeDutyCycle(0)
                last_detected = False

            cv2.imshow("Sun Tracker", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        last_detected = True

        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if cls_id == 0 and conf > 0.5:  # ปรับความมั่นใจเป็น 50%
                x1, y1, x2, y2 = box.xyxy[0]

                if any(map(lambda v: v is None or v != v, [x1, y1, x2, y2])):
                    continue

                x_center = (x1 + x2) / 2

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(x_center), int((y1 + y2) / 2)), 5, (0, 0, 255), -1)

                offset_x = x_center - center_x_img

                if abs(offset_x) > deadzone_threshold:
                    # คำนวณการปรับมุมจากตำแหน่งปัจจุบัน
                    adjustment_angle = (offset_x / width) * 120  # ปรับตามสัดส่วนความกว้างของภาพ
                    current_pan_angle += adjustment_angle
                    current_pan_angle = max(0, min(120, current_pan_angle))  # จำกัดมุมไม่เกิน 0-120 องศา

                    duty_cycle = angle_to_duty_cycle(current_pan_angle)
                    pan_servo.ChangeDutyCycle(duty_cycle)

                    print(f"Detected Sun - X Center: {x_center}, Pan Angle: {current_pan_angle:.1f}, Duty Cycle: {duty_cycle:.2f}")

                conf_percent = conf * 100
                text_info = (f"X Center=({int(x_center)}) Pan={current_pan_angle:.1f} Conf={conf_percent:.1f}%")
                cv2.putText(frame, text_info, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Sun Tracker", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print("โปรแกรมหยุดการทำงานด้วย Keyboard Interrupt")

finally:
    cap.release()
    cv2.destroyAllWindows()
    if pan_servo is not None:
        pan_servo.stop()
    GPIO.cleanup()
