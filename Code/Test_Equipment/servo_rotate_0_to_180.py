import RPi.GPIO as GPIO
import time

SERVO_PIN = 18  # ใช้ GPIO18 (BCM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

สร้าง PWM ที่ความถี่ 50Hz (เหมาะกับ Servo ทั่วไป)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)  # เริ่มต้นที่ duty cycle = 0

def set_servo_angle(angle):
    """ฟังก์ชันปรับมุม Servo (0-180 องศา)"""
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)  # หน่วงเวลาให้เซอร์โวหมุนทัน
    pwm.ChangeDutyCycle(0)  # หยุดจ่าย PWM ค้าง (ลดการสั่น/ความร้อน)

try:
    while True:
        # หมุนจาก 0 ถึง 180 องศา ทีละ 30 องศา
        for angle in range(0, 181, 30):
            print(f"Set angle to {angle}")
            set_servo_angle(angle)
            time.sleep(1)

        # หมุนจาก 180 กลับไป 0 องศา
        for angle in range(180, -1, -30):
            print(f"Set angle to {angle}")
            set_servo_angle(angle)
            time.sleep(1)

except KeyboardInterrupt:
    # ถ้า user กด Ctrl+C ให้หยุด
    pass
finally:
    pwm.stop()
    GPIO.cleanup()