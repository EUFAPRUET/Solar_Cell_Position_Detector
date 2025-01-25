<a id="readme-top"></a>
# CPE-414 Solar Cell Positon Detector
<div align="center">

  <img src="assets/logo.png" alt="logo" width="200" height="auto" />
  <h1>Solar Cell Postion Detector</h1>
  
  <p>RTOS Project With Raspberry Pi 5 & Deep Learning</p>
</div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#sun_with_face-Overview">Overview</a></li>
        <li><a href="#mag-how-it-works">How It Works</a></li>
        <li><a href="#wrench-technologies-used">Technologies Useds</a></li>
      </ul>
    </li>
    <li>
      <a href="#requirements">Requirements</a>
      <ul>
        <li><a href="#receipt-functional-requirements">Functional Requirements</a></li>
        <li><a href="#receipt-Non-Functional-Requirements">Non-Functional Requirements</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center"><img src="Model/Solar_Cell_Position_Detector_Model_2_axis.jpg" alt="model" width="500" height="auto" /></div>

### :sun_with_face: Overview<br>
The Solar Cell Position Detector is an intelligent sun-tracking system designed to maximize solar energy efficiency by dynamically adjusting the position of a solar panel based on the real-time position of the sun. This project integrates Deep Learning, Computer Vision, and Servo Motor Control on a Raspberry Pi 5 to continuously track the sun and reposition the solar panel accordingly.

### :mag: How It Works
1. Real-Time Sun Detection
   - A camera module captures live images of the sky.
   - A Deep Learning model (YOLO/SSD) or OpenCV-based processing detects the sun’s position.
2. Automated Camera Tracking
   - A servo-controlled camera dynamically adjusts its angle to keep the sun centered in the frame.
3. Solar Panel Alignment
   - The system calculates the optimal tilt and rotation angle for the solar panel.
   - Servo/Stepper motors adjust the solar panel’s position to follow the sun throughout the day.
  
### :wrench: Technologies Used
- Hardware
  - Raspberry Pi 5 – Main processing unit
  - Camera Module – Captures real-time images
  - Servo Motors – Adjust the camera and solar panel’s position
  - Solar Panel – Mounted on an adjustable tracking system
  - ND/Solar Filter – Prevents excessive sunlight damage
- Software & AI
  - Deep Learning (YOLOv5, YOLOv8, SSD-MobileNet) – Sun detection
  - OpenCV – Image processing & tracking
  - Python (RPi.GPIO, pigpio) – Servo motor control
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Requirements
### :receipt: Functional Requirements 
1. Image Processing & Sun Detectionn
   - [x] The system captures real-time images of the sky using a camera module.
   - [x] The system detects the sun’s position in the image using a trained Deep Learning model (YOLO/SSD) or image processing techniques (OpenCV-based filtering, Hough Transform, etc.).
   - [x] The system calculates the offset of the sun from the center of the frame.
   - [x] The system continuously updates detection in real-time to track the sun’s movement.
2. Servo Motor Control
   - [ ] The system sends servo control signals based on the detected sun position.
   - [ ] The camera module adjusts itself to keep the sun at the center of the frame.
   - [ ] The system calculates the optimal angle for the solar panel based on the camera’s orientation.
   - [ ] The solar panel automatically rotates and tilts to match the detected sun’s position.
3. System Integration & Communication
   - [x] The Raspberry Pi 5 serves as the main processing unit for image detection and motor control.
   - [x] The servo motors (Pan & Tilt) and solar panel actuator receive control signals from the Raspberry Pi via GPIO/PWM.

### :receipt: Non-Functional Requirements
1. Performance
   - [x] The system should maintain real-time sun tracking (at least 5-10 FPS).
   - [ ] The servo control should have minimal delay (<1 sec) to ensure smooth tracking.
   - [ ] The system should work in various lighting conditions (e.g., clear sky, cloudy conditions).
2. Hardware Reliability
   - [ ] The camera module should handle intense sunlight without damage (e.g., using ND Filter or Solar Filter).
   - [x] The servo motors should be strong enough to rotate the solar panel smoothly.
   - [x] The Raspberry Pi should be properly powered to avoid overheating or voltage drops.
3. Scalability & Expandability
   - [x] The system should be modular, allowing upgrades for better AI models, additional sensors, or larger panels.
   - [x] The software should allow future integration with additional light sensors, cloud data logging, or an IoT dashboard.
4. Power Efficiency
   - [x] The entire system should consume minimal power, making it viable for off-grid solar applications.
   - [x] If possible, the Raspberry Pi and servo motors should be powered by the solar panel itself.
<p align="right">(<a href="#readme-top">back to top</a>)</p>
