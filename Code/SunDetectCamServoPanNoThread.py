import cv2
import time
import threading
import RPi.GPIO as GPIO
from ultralytics import YOLO

# ====== GPIO Setup for Servo Motor ======
PAN_SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PAN_SERVO_PIN, GPIO.OUT)
pan_servo = GPIO.PWM(PAN_SERVO_PIN, 50)

# เริ่มต้นเซอร์โวที่ตำแหน่งกลาง (Duty Cycle ประมาณ 7 => ~90 องศา)
pan_servo.start(7)
time.sleep(0.4)
pan_servo.ChangeDutyCycle(0)

def angle_to_duty_cycle(angle):
    """แปลงองศา (0-180) ไปเป็น Duty Cycle (ประมาณ 2 - 12)"""
    return 2 + (angle / 18.0)

# ====== YOLO Model ======
model = YOLO("SunDetectionModel.pt")

# ====== Global Variables (แชร์ระหว่าง Thread) ======
latest_frame = None        # เก็บเฟรมล่าสุดจากกล้อง
latest_boxes = []          # เก็บผลการตรวจจับรอบล่าสุด
stop_program = False       # Flag สำหรับสั่งให้ทุก Thread หยุด
detection_done = False     # บอกว่า "รอบตรวจจับ" ล่าสุดเสร็จแล้ว

# ====== การตั้งค่า ======
width = 640
center_x_img = width // 2
deadzone_threshold = 0
pan_angle = 90

# เวลารอระหว่างการตรวจจับ (วินาที)
DETECTION_INTERVAL = 10

# ====== Camera Thread ======
class CameraThread(threading.Thread):
    def __init__(self, camera_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print("ไม่สามารถเปิดกล้องได้")

    def run(self):
        global latest_frame, stop_program
        while not stop_program:
            ret, frame = self.cap.read()
            if not ret:
                continue
            # เก็บเฟรมลงตัวแปร
            latest_frame = frame
        
        self.cap.release()
        print("Camera Thread stopped.")

# ====== Detection Thread (ตรวจจับทุก ๆ DETECTION_INTERVAL วินาที) ======
class DetectionThread(threading.Thread):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.last_detection_time = 0

    def run(self):
        global stop_program, latest_frame, latest_boxes, detection_done

        while not stop_program:
            current_time = time.time()
            # หากเวลาห่างจากการตรวจครั้งก่อน >= DETECTION_INTERVAL
            if (current_time - self.last_detection_time) >= DETECTION_INTERVAL:
                # ต้องแน่ใจว่ามีภาพจากกล้องก่อน
                if latest_frame is not None:
                    print("[DetectionThread] Start detection...")
                    results = self.model.predict(latest_frame, conf=0.5)
                    latest_boxes = results[0].boxes
                    detection_done = True  # บอกว่าเสร็จการตรวจจับแล้ว
                    self.last_detection_time = current_time

                # จะไม่ตรวจจับซ้ำทันที แต่จะรอครบ 20 วิอีกครั้ง
            time.sleep(0.1)  # พักสั้น ๆ ลดการใช้ CPU

        print("Detection Thread stopped.")

# ====== Main ======
def main():
    global stop_program, detection_done, latest_boxes, pan_angle

    # สร้าง Thread
    camera_thread = CameraThread(0)
    detection_thread = DetectionThread(model)

    # เริ่ม Thread
    camera_thread.start()
    detection_thread.start()

    try:
        while True:
            if latest_frame is None:
                # รอให้กล้องเริ่มส่งภาพ
                time.sleep(0.01)
                continue

            # ทำสำเนาภาพล่าสุดมาแสดงผล
            frame = latest_frame.copy()

            # หากรอบตรวจจับล่าสุดเสร็จแล้ว (detection_done == True)
            # ก็อ่านผลกล่องมาแสดงและสั่งเซอร์โว
            if detection_done:
                # ประมวลผลกล่องเฉพาะรอบล่าสุดเพียงครั้งเดียว
                if len(latest_boxes) > 0:
                    for box in latest_boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])

                        # สมมติ label 0 คือ Sun
                        if cls_id == 0 and conf > 0.5:
                            x1, y1, x2, y2 = box.xyxy[0]
                            # ตรวจสอบ NaN หรือ None
                            if any(map(lambda v: v is None or v != v, [x1, y1, x2, y2])):
                                continue

                            x_center = (x1 + x2) / 2
                            offset_x = x_center - center_x_img

                            # วาดกรอบ + จุดกึ่งกลาง
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                          (0, 255, 0), 2)
                            cv2.circle(frame, (int(x_center), int((y1 + y2) / 2)), 5,
                                       (0, 0, 255), -1)

                            # หมุนเซอร์โวถ้าอยู่นอก deadzone
                            if abs(offset_x) > deadzone_threshold:
                                pan_angle = 180 * (x_center / width)
                                pan_angle = max(0, min(180, pan_angle))

                                duty_cycle = angle_to_duty_cycle(pan_angle)
                                pan_servo.ChangeDutyCycle(duty_cycle)
                                time.sleep(0.4)
                                pan_servo.ChangeDutyCycle(0)

                                print(f"[MainThread] Detected Sun - X Center: {x_center}, "
                                      f"Pan Angle: {pan_angle:.1f}, Duty Cycle: {duty_cycle:.2f}")

                            # แสดงค่าบนภาพ
                            conf_percent = conf * 100
                            text_info = f"X Center=({int(x_center)}) Pan={pan_angle:.1f} Conf={conf_percent:.1f}%"
                            cv2.putText(frame, text_info, (10, 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), 2, cv2.LINE_AA)

                # ตั้งค่าว่าเสร็จแล้ว จะไม่ประมวลผลซ้ำจนกว่าจะมี detection รอบถัดไป
                detection_done = False

            # แสดงภาพ
            cv2.imshow("Sun Tracker", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # กด ESC เพื่อออก
                break

    except KeyboardInterrupt:
        print("[Main] KeyboardInterrupt, stopping...")

    finally:
        # สั่งให้ Threads หยุด
        stop_program = True
        camera_thread.join()
        detection_thread.join()

        cv2.destroyAllWindows()
        pan_servo.stop()
        GPIO.cleanup()

        print("[Main] Program terminated.")

if __name__ == "__main__":
    main()