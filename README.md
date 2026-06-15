# License Plate Recognition

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Haar%20Cascade-green)
![Tesseract](https://img.shields.io/badge/OCR-Tesseract-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A desktop GUI tool that detects an Indian vehicle number plate in an image using a classical
OpenCV **Haar cascade**, reads the characters with **Tesseract OCR**, and looks up the issuing
state/UT from the plate's first two characters.

> **Note:** This is a classical computer-vision + OCR pipeline. It does **not** use deep learning,
> and no model is trained — detection relies on a pre-trained Haar cascade and recognition on the
> Tesseract OCR engine.

## Sample Input

A sample car image from [`Data/`](Data) — the app detects the plate region and reads `DL 7CQ 1939`,
resolving the `DL` prefix to **Delhi**:

![Sample car image](Data/image01.jpg)

## Features

- Simple Tkinter GUI to upload a car image and view results.
- Number-plate region detection via OpenCV's Haar feature-based cascade classifier.
- Light image pre-processing (crop, dilate/erode, grayscale, binary threshold) to improve OCR.
- Character recognition with the Tesseract OCR engine via `pytesseract`.
- State/UT lookup from the first two characters of the recognised plate text.
- Annotated output: the detected plate is boxed and labelled on the original image, and the
  cropped plate is saved as `Number Plate.jpg`.

## Tech Stack

- **Python 3** — application language
- **Tkinter** — desktop GUI (ships with the standard library)
- **OpenCV (`opencv-python`)** — image processing and Haar cascade detection
- **Tesseract OCR** (via **`pytesseract`**) — optical character recognition
- **NumPy** — array/kernel operations for pre-processing
- **Pillow (`PIL`)** — image loading/display in the GUI

## How It Works

1. **Upload** — the user selects a car image through the GUI file dialog.
2. **Detect** — the image is converted to grayscale and `haarcascade_russian_plate_number.xml`
   locates the plate region (`detectMultiScale`).
3. **Pre-process** — the plate region is cropped, dilated/eroded, grayscaled and binary-thresholded.
4. **Recognise** — Tesseract OCR (`pytesseract.image_to_string`) reads the characters; non-alphanumeric
   characters are stripped.
5. **Lookup** — the first two characters are matched against a dictionary of Indian state/UT codes.
6. **Display** — the original image is annotated with the plate text, and the cropped plate plus the
   resolved state are shown in the GUI.

## Prerequisites

- Python 3.8+
- **Tesseract OCR engine** installed as a system binary (it is *not* a pip package):
  - **macOS:** `brew install tesseract`
  - **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
  - **Windows:** install from the [UB-Mannheim build](https://github.com/UB-Mannheim/tesseract/wiki);
    the script auto-detects the default path `C:/Program Files/Tesseract-OCR/tesseract.exe`.
- On macOS/Linux the `tesseract` binary must be on your `PATH` (the package installers above handle this).

## Installation

```bash
git clone https://github.com/archiskhuspe/license-plate-recognition.git
cd license-plate-recognition
pip install -r requirements.txt
```

## Usage

```bash
python license_plate_recognition.py
```

1. Click **Upload an image** and pick a car image (sample images are in [`Data/`](Data)).
2. Click **Classify Image**.
3. The recognised plate text and matched state appear alongside the cropped plate.

## Project Structure

```
license-plate-recognition/
├── license_plate_recognition.py            # Tkinter GUI app + detection/OCR pipeline
├── haarcascade_russian_plate_number.xml    # Pre-trained Haar cascade for plate detection
├── requirements.txt                        # Python dependencies
├── Data/                                   # Sample car images for testing
├── license_plate_recognition_report.docx   # Project report
├── LICENSE
└── README.md
```

## Limitations

- **Not deep learning.** Detection uses a pre-trained Haar cascade and recognition uses Tesseract;
  nothing is trained in this project.
- The bundled cascade is the generic "Russian plate" model, so detection is **hit-or-miss** on
  varied angles, lighting, distances and plate styles.
- OCR accuracy depends heavily on image quality; blurry, skewed or low-contrast plates often misread.
- The state lookup is a **naive** match on the first two characters and does not validate the full
  Indian plate format.
- Desktop-only, single-image tool — no batch processing, video, or API.
- The Tesseract install path is auto-detected on Windows; other platforms rely on `tesseract` being
  on `PATH`.

## License

Released under the [MIT License](LICENSE).
