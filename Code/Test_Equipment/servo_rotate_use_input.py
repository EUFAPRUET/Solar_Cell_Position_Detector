import RPi.GPIO as GPIO
import time

# GPIO pin for the single servo motor (Pan)
SERVO_PIN = 18  # BCM 18

# Initial angle for the pan servo
pan_angle = 90

# Step size (in degrees) to increment or decrement the servo angle
ANGLE_STEP = 5

def setup_servo():
    """
    Sets up GPIO and initializes the servo on the specified pin (SERVO_PIN).
    Assumes a 50Hz PWM frequency for typical hobby servos (e.g., SG90, MG90S).
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    servo_pan = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
    servo_pan.start(0)  # Start with 0% duty cycle
    return servo_pan

def set_servo_angle(servo, angle):
    """
    Converts a given angle (0 to 180 degrees) into an approximate duty cycle
    for a typical servo. Then updates the servo's position accordingly.
    
    :param servo: The PWM object for the servo
    :param angle: The target angle (0-180 degrees)
    """
    duty = 2.0 + (angle / 18.0)  # Convert angle to duty cycle (approx. for SG90)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.2)
    # Uncomment if you want to stop sending PWM after moving:
    # servo.ChangeDutyCycle(0)

def main():
    global pan_angle

    servo_pan = setup_servo()

    print("=== Single Axis Servo Test (Pan) ===")
    print("Press 'a' to pan left (increase angle)")
    print("Press 'd' to pan right (decrease angle)")
    print("Press 'q' to quit")

    try:
        while True:
            cmd = input("Enter command (a/d/q): ").strip().lower()

            if cmd == 'q':
                print("Quitting program.")
                break

            elif cmd == 'a':
                # Pan left => increase angle
                pan_angle += ANGLE_STEP
                if pan_angle > 180:
                    pan_angle = 180
                set_servo_angle(servo_pan, pan_angle)
                print(f"Pan Angle: {pan_angle}")

            elif cmd == 'd':
                # Pan right => decrease angle
                pan_angle -= ANGLE_STEP
                if pan_angle < 0:
                    pan_angle = 0
                set_servo_angle(servo_pan, pan_angle)
                print(f"Pan Angle: {pan_angle}")

            else:
                print("Invalid command! Use 'a', 'd', or 'q' only.")

    except KeyboardInterrupt:
        pass
    finally:
        servo_pan.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()