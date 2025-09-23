# Real-Time Camera Processing with Kivy & OpenCV

A real-time camera processing application built with Kivy, OpenCV, and NumPy that provides various image filters and effects.

## Features

- Real-time camera feed display
- Multiple image processing filters:
  - Grayscale conversion
  - Gaussian blur
  - Edge detection (Canny)
  - Image sharpening
  - Emboss effect
  - Sepia tone
  - Color inversion
  - HSV color thresholding (blue detection)
- Start/Stop camera controls
- User-friendly GUI with filter selection buttons

## Requirements

- Python 3.7+
- Camera/webcam connected to your system

## Installation

1. Clone or download this project
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

### Controls

- **Start Camera**: Begin capturing video from your default camera
- **Stop Camera**: Stop the video feed
- **Filter Buttons**: Apply different image processing effects in real-time

### Available Filters

1. **None**: Original camera feed
2. **Grayscale**: Convert to black and white
3. **Blur**: Apply Gaussian blur effect
4. **Edge Detection**: Highlight edges using Canny algorithm
5. **Sharpen**: Enhance image sharpness
6. **Emboss**: Create embossed effect
7. **Sepia**: Apply vintage sepia tone
8. **Invert**: Invert all colors
9. **Blue HSV**: Detect and highlight blue objects

## Technical Details

The application uses:
- **Kivy**: For the GUI framework and real-time display
- **OpenCV**: For camera capture and image processing
- **NumPy**: For efficient array operations and custom filters

## Troubleshooting

- Ensure your camera is not being used by another application
- Check that your camera permissions are enabled
- Verify all dependencies are installed correctly