# Project-Ledz-Cube
This repository contains the code developed for the Ledz Cube Project by my group for the Computer Engineering introduction subject (PCS3100) at the University of São Paulo.

It consists of a Rubik's Cube made of LED strips that can be manipulated using a motion capture system with a laptop camera. The Rubik's Cube can be altered through a mobile app, which includes functions like shuffling the Rubik's Cube, executing moves, showing the last move, and initializing the Rubik's Cube.

Among the technologies used, the following are noteworthy: Raspberry Pi 3 microcontroller with Raspbian OS, a laptop camera, LED strips, Python with specialized libraries, Firebase Cloud Storage, and MIT App Inventor.

For the motion capture system, OpenCV and MediaPipe libraries were used to detect hand movements that correspond to certain Rubik's Cube moves. This information is sent to Firebase Cloud Storage using the Pyrebase Python library. The data can be accessed by the mobile app directly from Firebase Storage, just as information can be sent from the app.

In the Raspberry Pi 3 microcontroller, a Python script is used to access information from the cloud storage with the Firebase Admin library, interpret the data, and change the LED strip accordingly using the rpi_ws281x library.
