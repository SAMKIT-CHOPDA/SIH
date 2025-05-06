# 🚦 Smart AI-Based Traffic Signal Management System – SIH 2024

An intelligent real-time traffic management system designed for Smart India Hackathon 2024. This project aims to dynamically control traffic signals using AI-based vehicle detection and microcontroller integration to reduce congestion, pollution, and response time at urban intersections.

## 🔧 Project Overview

- **Name:** AI Traffic Signal Management System
- **Event:** Smart India Hackathon 2024 (SIH)
- **Category:** Smart Automation
- **Status:** Completed

## 🎯 Objective

To design and implement a scalable, cost-effective traffic signal system that:
- Detects the number of vehicles on each lane in real-time.
- Dynamically allocates green signal time based on vehicle density.
- Operates autonomously using ESP32s, OpenCV, and a centralized Raspberry Pi.
- Improves traffic flow and reduces idle engine emissions.

## 🧠 Core Technologies

| Layer         | Technologies Used                             |
|--------------|------------------------------------------------|
| Hardware      | ESP32, Raspberry Pi 4, IR Sensors, Cameras     |
| Software      | Python (OpenCV, NumPy), Arduino (C++), Flask   |
| Communication | Wi-Fi (ESP-NOW or MQTT), Serial/UART           |
| AI/ML (optional) | Object Detection Models (YOLOv5 or Haarcascade) |

## 📈 System Architecture

1. **ESP32 Devices (x4):** Installed on each lane to count vehicles.
2. **Central Raspberry Pi Unit:** Receives data and computes the optimal green light duration.
3. **Signal Control Logic:** Yellow light for 3 seconds before switching lanes in a circular fashion.
4. **Optional Web Dashboard:** To monitor real-time status and logs.

## 🔄 Signal Cycle Logic

1. Count vehicles in Lane A → Assign green time based on density.
2. Switch to yellow for 3 seconds.
3. Repeat for Lanes B, C, and D.
4. Loop continuously with dynamic updates.

## 🚀 Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/sih-traffic-system.git

2. Install required Python libraries:
    pip install opencv-python flask numpy
    Upload Arduino sketch to ESP32s for vehicle counting.

3. Run Raspberry Pi controller script:
     python3 main_controller.py
