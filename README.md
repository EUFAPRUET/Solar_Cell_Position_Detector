<a id="readme-top"></a>
# CPE-414 Solar Cell Positon Detector
<div align="center">

  <img src="assets/logo.png" alt="logo" width="300" height="auto" />
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
        <li><a href="#page_facing_up-functional-requirements">Functional Requirements</a></li>
        <li><a href="#page_with_curl-Non-Functional-Requirements">Non-Functional Requirements</a></li>
      </ul>
    </li>
    <li>
      <a href="#dataset-references">Dataset References</a>
      <ul>
        <li><a href="#open_file_folder-dataset-selection-and-usage">Dataset Selection And Usage</a></li>
        <li><a href="#bar_chart-dataset-types">Dataset Types</a></li>
        <li><a href="#hammer_and_wrench-dataset-preprocessing-and-annotation">Dataset Preprocessing And Annotation</a></li>
      </ul>
    </li>
    <li>
      <a href="#yolo-model-for-sun-detection">YOLO Model for Sun Detection</a>
      <ul>
        <li><a href="#bookmark-model-selection">Model Selection</a></li>
        <li><a href="#mortar_board-training-process">Training Process</a></li>
        <li><a href="#microscope-model-evaluation">Model Evaluation</a></li>
      </ul>
    </li>
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
### :page_facing_up: Functional Requirements 
1. Image Processing & Sun Detectionn
   - The system captures real-time images of the sky using a camera module.
   - The system detects the sun’s position in the image using a trained Deep Learning model (YOLO/SSD) or image processing techniques (OpenCV-based filtering, Hough Transform, etc.).
   - The system calculates the offset of the sun from the center of the frame.
   - The system continuously updates detection in real-time to track the sun’s movement.
2. Servo Motor Control
   - The system sends servo control signals based on the detected sun position.
   - The camera module adjusts itself to keep the sun at the center of the frame.
   - The system calculates the optimal angle for the solar panel based on the camera’s orientation.
   - The solar panel automatically rotates and tilts to match the detected sun’s position.
3. System Integration & Communication
   - The Raspberry Pi 5 serves as the main processing unit for image detection and motor control.
   - The servo motors (Pan & Tilt) and solar panel actuator receive control signals from the Raspberry Pi via GPIO/PWM.

### :page_with_curl: Non-Functional Requirements
1. Performance
   - The system should maintain real-time sun tracking (at least 5-10 FPS).
   - The servo control should have minimal delay (<1 sec) to ensure smooth tracking.
   - The system should work in various lighting conditions (e.g., clear sky, cloudy conditions).
2. Hardware Reliability
   - The camera module should handle intense sunlight without damage (e.g., using ND Filter or Solar Filter).
   - The servo motors should be strong enough to rotate the solar panel smoothly.
   - The Raspberry Pi should be properly powered to avoid overheating or voltage drops.
3. Scalability & Expandability
   - The system should be modular, allowing upgrades for better AI models, additional sensors, or larger panels.
   - The software should allow future integration with additional light sensors, cloud data logging, or an IoT dashboard.
4. Power Efficiency
   - The entire system should consume minimal power, making it viable for off-grid solar applications.
   - If possible, the Raspberry Pi and servo motors should be powered by the solar panel itself.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Dataset References
### :open_file_folder: Dataset Selection And Usage
The Solar Cell Position Detector requires a high-quality dataset to train its Deep Learning model for accurate real-time sun detection under various lighting and weather conditions. The dataset selection and preprocessing are crucial to ensuring reliable tracking performance.

### :bar_chart: Dataset Types
1. Open Datasets (Public Sources)
   <br>If available, publicly accessible datasets can be used to improve model accuracy:
   - [Roboflow Universe-sun_detection Computer Vision Project](https://universe.roboflow.com/scene/sun_detection/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true) - Contains various images of the sky and sun.
   - [Roboflow Universe-Sun Tracking Computer Vision Project](https://universe.roboflow.com/suntrack/sun-tracking/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true) - Contains various images of the sky and sun.
   - [Kaggle-Sun and moon images ](https://www.kaggle.com/datasets/khushipitroda/sun-and-moon-images) - Contains various images of the sky, sun and moon.
   - Weather & Atmospheric Image Databases - Various sources providing satellite and sky images.
2. Custom Dataset (Self-Collected)
   <br>If no suitable public dataset exists, we collect images manually:
   - Capturing real-time sky images using the Raspberry Pi Camera Module at different times of the day.
   - Data collected under various weather conditions (clear sky, cloudy, sunrise, sunset).
   - Ensuring diverse dataset coverage for better generalization in real-world applications.
3. Synthetic Data & Augmentation
   <br>To increase dataset robustness, we apply:
   - Data Augmentation: Adjusting brightness, contrast, blurring, rotation, and noise.
   - Synthetic Image Generation: Simulating sun positions in different sky environments.

### :hammer_and_wrench: Dataset Preprocessing And Annotation
1. Labeling the Dataset
   <br>For Deep Learning Object Detection Models (YOLO, SSD, etc.), each image is annotated with bounding boxes around the sun.
   - Annotation Tools:
     - [LabelImg](https://github.com/HumanSignal/labelImg) (Manual bounding box annotation)
     - [Roboflow](https://roboflow.com/) (Dataset management & augmentation)
2. Dataset Format
   - Image Formats: .jpg, .png
   - Annotation Formats: .txt (YOLO format), .xml (Pascal VOC), .json (COCO format)
3. Dataset Splitting Strategy <br>
   | Dataset Partition  | Percentage |
   | ------------- | ------------- |
   | Training Data | 80% |
   | Validation Data  | 10%  |
   | Testing Data  | 10%  |
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## YOLO Model for Sun Detection
### :bookmark: Model Selection
For sun detection, we utilized YOLOv8 Nano, a lightweight yet powerful model optimized for real-time object detection on edge devices like the Raspberry Pi 5. This model was selected due to its:
- High detection accuracy even in varied lighting conditions.
- Fast inference time suitable for real-time applications.
- Compatibility with resource-constrained hardware.

### :mortar_board: Training Process
Dataset Preparation:
- Images were collected under various weather conditions (clear, cloudy, sunrise, sunset).
- Annotations were done using Roboflow and saved in YOLO format.

Model Configuration:
- Pre-trained YOLOv8 weights were fine-tuned on the sun detection dataset.
- Hyperparameters were adjusted to improve detection accuracy:
  - Batch size: 16
  - Learning rate: 0.001
  - Epochs: 50

Training Environment:
- Training was performed on a machine with GPU acceleration.
- Final model was exported in .pt format for deployment on the Raspberry Pi.

### :microscope: Model Evaluation
- Accuracy: Achieved over 95% detection accuracy on test data.
- Performance: Real-time inference at 5-10 FPS on the Raspberry Pi 5.
- Robustness: Model performed well in varying light conditions, including partial cloud cover.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Hardware Setup
### :gear: Hardware Components
1. Raspberry Pi 5 <br>
  The main processing unit that runs the YOLO model, processes the camera input, and controls the servo motors.
2. Camera Module <br>
  Used to capture real-time images of the sky for sun detection. A standard Raspberry Pi Camera Module or compatible USB camera can be used.
3. Servo Motors (e.g. SG90 ,RDS3115) <br>
  Responsible for adjusting the position of the camera and the solar panel to keep the sun centered in the frame. High-torque servo motors are recommended for stable and smooth movement.
4. Solar Panel <br>
  Mounted on a movable frame, allowing dynamic positioning to maximize sunlight exposure throughout the day.
5. ND/Solar Filter <br>
  Used to protect the camera lens from intense sunlight, ensuring clear image capture without damage.
6. Supporting Components <br>
    - Wires & Connectors: For connecting components to the Raspberry Pi.
    - Mounting Brackets: To securely mount the camera and solar panel.
    - Breadboard (optional): For prototyping and testing connections.

### :electric_plug: Hardware Connections
1. Connecting the Camera:
    - Attach the camera module to the CSI port on the Raspberry Pi or connect a USB camera
2. Servo Motor Connections:
    - Signal Wire (Orange/White): Connect to GPIO18 (PWM) on Raspberry Pi.
    - Power Wire (Red): Connect to a 5V power source.
    - Ground Wire (Brown/Black): Connect to the GND pin on Raspberry Pi.
3. Solar Panel Mounting:
    - Mount the solar panel onto the servo-controlled frame.
    - Ensure the servo motors are calibrated for full 180° rotation.





[@titichaya](https://github.com/titichaya) - Adviser
<br>[@EUFAPRUET](https://github.com/EUFAPRUET) - Hardware Developer
<br>[@TechTnKorn](https://github.com/TechTnKorn) - Ai Developer
<br>[@ukp_alex](https://github.com/UkpAlex) - Ai Developer
<br>[@Pr.Chanaradee](https://github.com/pr-chanaradee) - Project Manager
<br>[@fordisacar](https://github.com/fordisacar) - Coordinator

