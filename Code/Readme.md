# AI Exercise Assistant

> A real-time pose estimation and exercise feedback system built with MoveNet Thunder and TensorFlow.

---

## Overview

Using machine learning and computer vision, this application provides real-time visual feedback on exercise form without requiring specialist equipment or professional supervision. A standard webcam captures the user's movements, the MoveNet Thunder pose estimation model tracks key joints, and a traffic-light feedback mechanism guides the user into the correct position in real time.

The project was motivated by a real-world problem: many physiotherapy patients struggle to perform exercises correctly when unsupervised, which can slow recovery or risk further injury. This system demonstrates that high-quality pose estimation and real-time feedback are achievable on standard consumer hardware.

---

## Features

- **Real-time pose estimation** using MoveNet Thunder, tracking shoulder, elbow, and wrist landmarks at sub-100ms latency
- **Traffic-light feedback** that colour-codes visual cues dynamically based on joint angle during movement
- **Repetition counting** that automatically tracks completed reps against a user-defined target
- **Performance scoring** calculated out of 100% based on peak and rest angle consistency and completion ratio
- **Analytics dashboard** displaying line, bar, and radar charts that visualise duration trends, completion rates, and overall performance across sessions
- **Exercise history** presented as a scrollable records table with per-session metrics including score, angles, form consistency, and duration
- **Threaded model loading** that initialises the camera and model on a background thread, keeping the interface responsive

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3 |
| Pose estimation | TensorFlow Lite — MoveNet Thunder |
| GUI | Tkinter |
| Data visualisation | Matplotlib, Pandas |
| Camera input | OpenCV |
| Data storage | CSV |

---

## Project Structure

```
ai-exercise-assistant/
├── HomeScreen.py          # Analytics dashboard and entry point
├── ChooseExercises.py     # Exercise selection and model loading
├── Camera.py              # Live camera feed, pose estimation, and feedback loop
├── Records.py             # Exercise history viewer
├── exercise_data.csv      # Session data store
├── assets/
│   ├── home_icon.png
│   └── back_icon.png
├── models/
│   ├── MoveNet_Thunder.tflite
│   └── MoveNet_lightning.tflite
└── requirements.txt
```

---

## How to Run

### Prerequisites

- Python 3.9+
- A webcam

### Install dependencies

```bash
pip install -r requirements.txt
```

### Launch

```bash
python HomeScreen.py
```

The app opens in fullscreen. Use the **Choose Exercise** button to begin a session, or **View Records** to review past sessions.

---

## How It Works

1. The user selects an exercise and sets a target rep count
2. MoveNet Thunder runs inference on each camera frame to extract 17 body landmarks
3. The elbow joint angle, calculated from shoulder, elbow, and wrist positions, is computed per frame
4. Angle thresholds classify the position as correct (green), borderline (amber), or incorrect (red)
5. The rep count increments when the joint completes a full peak-to-rest cycle
6. On completion, a session score is calculated and written to `exercise_data.csv`
7. The dashboard charts update to reflect the new session

---

## Evaluation Results

Tested with a group of student participants using a structured Likert-scale survey:

| Metric | Mean Likert Score |
|---|---|
| Interface usability | 4.08 / 5 |
| Performance scoring | 3.68 / 5 |
| ML accuracy | 3.36 / 5 |

Latency consistently remained below **100ms** on standard consumer hardware, and repetition counting proved accurate across varied lighting conditions. The main limitation encountered was that tracking degraded when loose or baggy sleeves obscured joint landmarks.

---

## Limitations and Future Work

The current implementation supports **right arm curls** only, though the architecture is designed to accommodate additional exercises. Joint detection is less reliable with loose clothing or poor lighting, which future work could address by integrating IMU sensors for more precise joint angle measurement. Extending the system to a clinical rehabilitation setting with an expanded exercise library and multimodal sensing represents the most promising long-term direction.

---

## Methodology

This project was developed using a hybrid Waterfall–Agile approach, where fixed milestones defined the project phases while iterative cycles with supervisor reviews allowed rapid responses to technical challenges such as model integration and thread management.