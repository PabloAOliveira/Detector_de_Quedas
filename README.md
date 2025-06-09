# Fall Detector 🚨

A real-time fall detection system using computer vision and pose estimation to monitor and alert when a person falls.

## 📋 Overview

This project implements a fall detection system that uses your computer's camera to monitor a person's posture in real-time. Using MediaPipe's pose estimation, it analyzes body landmarks to detect potential falls based on body orientation and position changes.

## ✨ Features

- **Real-time monitoring**: Continuous monitoring using your camera feed
- **AI-powered detection**: Uses MediaPipe for accurate pose estimation
- **Multi-criteria detection**: Combines body angle and height difference analysis
- **Visual feedback**: Live pose visualization with highlighted detection points
- **Alert system**: Console alerts when potential falls are detected
- **Clean architecture**: Organized using Domain-Driven Design principles

## 🏗️ Architecture

The project follows a clean architecture pattern with clear separation of concerns:

```
fallDetector/
├── application/           # Use cases and application logic
│   └── monitor_fall_use_case.py
├── domain/               # Business logic and entities
│   ├── entities/         # Domain entities (Person)
│   └── services/         # Domain services (Fall Detection)
├── infrastructure/       # External dependencies
│   ├── ai/              # AI/ML components (Pose Detection)
│   └── camera/          # Camera hardware interface
└── main.py              # Application entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- A working camera (webcam or built-in camera)
- macOS, Windows, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fallDetector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **For Raspberry Pi users:**
   ```bash
   pip install opencv-python-headless==4.8.1.78 mediapipe==0.10.9 numpy==1.23.5
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 🎮 Usage

1. **Start the application**: Run `python main.py`
2. **Position yourself**: Stand in front of the camera where your full body is visible
3. **Monitor the feed**: The application will display your camera feed with pose landmarks
4. **Fall detection**: When a fall is detected, you'll see an alert message in the console
5. **Exit**: Press 'q' in the camera window or Ctrl+C in the terminal to stop

## 🔧 Configuration

You can adjust the fall detection sensitivity by modifying the parameters in `FallDetectionService`:

```python
# In domain/services/fall_detection_service.py
def __init__(self, angle_threshold=30, height_threshold=0.3):
    self.angle_threshold = angle_threshold      # Angle in degrees
    self.height_threshold = height_threshold    # Height difference threshold
```

- **angle_threshold**: Lower values = more sensitive to body tilt
- **height_threshold**: Lower values = more sensitive to horizontal positioning

## 🧠 How It Works

The fall detection algorithm uses two main criteria:

1. **Body Angle Analysis**: Calculates the angle between shoulder and hip relative to vertical
   - Triggers when body becomes too horizontal (> 60° from vertical by default)

2. **Height Difference**: Measures the vertical distance between shoulder and hip
   - Triggers when this distance becomes too small (person lying down)

### Detection Process

1. **Pose Estimation**: MediaPipe identifies body landmarks (shoulders, hips, etc.)
2. **Feature Extraction**: Key points are extracted for analysis
3. **Fall Analysis**: Multiple criteria are evaluated simultaneously
4. **Alert Generation**: Console alerts when fall conditions are met

## 📦 Dependencies

- **OpenCV**: Camera handling and image processing
- **MediaPipe**: AI-powered pose estimation
- **NumPy**: Numerical computations

## 🎯 Use Cases

- **Elderly Care**: Monitor elderly individuals for fall incidents
- **Healthcare Facilities**: Automated patient monitoring
- **Home Safety**: Personal safety monitoring system
- **Research**: Fall detection algorithm development and testing

## 🔍 Troubleshooting

### Camera Issues
- **Camera not found**: The system tries cameras 0, 1, and -1 automatically
- **Poor lighting**: Ensure adequate lighting for better pose detection
- **Multiple cameras**: System will automatically select the first working camera

### Performance Issues
- **High CPU usage**: Adjust the sleep time in `monitor_fall_use_case.py`
- **Slow detection**: Reduce camera resolution in `camera_service.py`

### Detection Issues
- **False positives**: Increase the threshold values
- **Missed detections**: Decrease the threshold values
- **Partial body visibility**: Ensure full body is visible in camera frame

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for the pose estimation framework
- [OpenCV](https://opencv.org/) for computer vision capabilities

## 📞 Support

If you encounter any issues or have questions, please open an issue in the repository.

---

**⚠️ Disclaimer**: This system is intended for monitoring and alerting purposes only. It should not be used as the sole safety system in critical applications. Always ensure proper medical and safety protocols are in place.
