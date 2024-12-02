# Bus-App
## Overview

The Sri Lanka Intelligent Bus Navigation and Passenger Information System is a project aimed at enhancing public transportation in Sri Lanka. The system provides real-time bus tracking, accurate arrival time predictions, and several features to improve the travel experience, including bus identification, school van tracking, voice activation for accessibility, and personalized notifications for bus arrivals.

## Problem Statement

In Sri Lanka, while vehicle tracking technology exists, it lacks a comprehensive, user-friendly system that provides real-time information about bus locations and estimated arrival times. Our system addresses these challenges by allowing users to:

- View exact arrival times for buses at their location or a delivery point, reducing unnecessary waiting time.
- Track school vans for parents, ensuring the safety and timely arrival of children.
- Verify the bus identity with images to ensure passengers board the correct vehicle.
- Use voice-activated commands for accessibility, particularly benefiting visually impaired users.
- Receive notifications about bus arrivals to avoid missed buses.

## Architectureal Diagram

![Untitled design (1)](https://github.com/user-attachments/assets/1c3568aa-27af-42ff-a104-311086632a9d)


## Project Components

### 1. IoT Device for Data Transfer
This component involves the development of firmware to collect vehicle data (location, speed, etc.) and transmit it to the Firebase server for real-time updates. The IoT device ensures accurate and efficient data collection from vehicles.

### 2. Secure Smart Card and Online Ticketing System
The system modernizes bus fare payments by implementing a reloadable smart card and an online ticketing platform. The system supports flexible payments and secure transactions through a Bitcoin-based payment platform. Users can recharge cards via the app and manage their ticket purchase history.

### 3. Real-Time ETA Prediction and Voice-Enabled User Interface
Using Firebase and server-side scripting, the system predicts the Estimated Time of Arrival (ETA) of buses based on historical data and real-time traffic conditions. The mobile app displays real-time vehicle locations and ETAs, including voice-enabled features to assist visually impaired users.

### 4. Smart Vehicle Identification and Alert System
This system captures images of vehicles and uses computer vision and OCR technologies to identify buses. The system handles multiple languages (Sinhala, Tamil, and English) and provides notifications for unauthorized vehicles or early/late arrivals. Users are alerted about the bus's status, helping them adjust their travel plans accordingly.  

## Features

- Real-Time Bus Tracking: View the exact location and arrival times of buses.
- Voice Activation: Use voice commands for easier accessibility, particularly for visually impaired users.
- Notifications: Receive real-time notifications about bus arrivals and any changes in the schedule.
- Text Recognition & Translation: Use OCR to detect and translate text from images in Sinhala, Tamil, and English.
- Smart Card and Online Ticketing: Pay bus fares securely and manage tickets through a smart card and online platform.

## Technologies Used

- IoT Devices (for vehicle data collection)
- Firebase (real-time database for vehicle tracking and data storage)
- Machine Learning (for ETA prediction)
- Computer Vision and OCR (for vehicle identification and text translation)
- Voice Recognition (for accessibility)
- Bitcoin-based Payment System (for secure transactions)
- Mobile App (user interface with real-time tracking and voice commands)  
