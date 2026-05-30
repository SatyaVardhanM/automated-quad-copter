# 🚁 Automated Quad Machine — AI Safety Companion Drone

> *"Technology should protect people, not just entertain them."*

A fully autonomous AI-powered quadcopter safety system built as a B.Tech major project at Malla Reddy College of Engineering (2020). Designed and implemented by **M. Satyavardhan**, this system combines real-time face recognition, NLP-based voice interaction, GPS-guided autonomous flight, and emergency alerting — all running on a Raspberry Pi.

---

## 🎯 Motivation

This project was conceived in response to growing safety concerns for individuals — particularly women — travelling alone at night. The goal was to build a low-cost, autonomous drone companion that could:

- Navigate autonomously to a registered user's location
- Verify their identity using facial recognition
- Engage them in voice conversation to confirm they are safe
- Automatically alert emergency contacts if the user is unresponsive or unrecognised

---

## ✅ What Was Actually Built & Tested

| Component | Status |
|---|---|
| Face detection & recognition (OpenCV + dlib) | ✅ Working |
| Voice chatbot (NLTK + TF-IDF + gTTS) | ✅ Working |
| Speech-to-text (Google Speech API) | ✅ Working |
| Autonomous GPS navigation (DroneKit) | ✅ Simulated via ArduPilot SITL |
| Full mission pipeline (face → chat → RTL) | ✅ Verified in simulation |

**Screenshots of the working system are in `/screenshots/`.**

---

## 🏗 System Architecture

```
User triggers drone via mobile/watch
           │
           ▼
  Drone arms & takes off (ArduPilot / DroneKit)
           │
           ▼
  Navigates to user's GPS coordinates (Neo-6M GPS)
           │
           ▼
  ┌─────────────────────────────┐
  │    Face Recognition         │  ← OpenCV + face_recognition (dlib)
  │    Camera + Haar Cascade    │
  └────────────┬────────────────┘
               │
       ┌───────┴────────┐
       │                │
   RECOGNISED      NOT RECOGNISED
       │                │
       ▼                ▼
  Voice Chatbot    EMERGENCY ALERT
  (NLTK + TF-IDF)  (SMS / call to contact)
  (gTTS + PyAudio)
       │
       ▼
  User confirms safe → Return to Launch
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.6+ |
| Face Recognition | `face_recognition` (dlib), OpenCV |
| NLP / Chatbot | NLTK, Scikit-learn (TF-IDF + Cosine Similarity) |
| Speech I/O | Google Speech API, gTTS, PyAudio |
| Drone Control | DroneKit (MAVLink / ArduPilot) |
| GPS | Neo-6M GPS Module |
| Hardware | Raspberry Pi 3B+, ISD1820 Mic, Camera Module |
| Simulation | ArduPilot SITL (Software in the Loop) |
| Wireless | Wi-Fi Module / LTE Modem |

---

## 📁 Project Structure

```
automated-quad-machine/
├── src/
│   ├── main.py              # Mission pipeline entry point
│   ├── face_detection.py    # Real-time face recognition
│   ├── speech.py            # TTS + STT audio I/O
│   └── chatbot.py           # NLP voice chatbot
├── faces/                   # Registered user face images (add your own)
│   └── README.md
├── screenshots/             # Proof of working simulation
│   ├── chatbot_working.png
│   ├── drone_idle.png
│   └── drone_reached_location.png
├── docs/
│   └── project_report.pdf
├── chatbot.txt              # Knowledge base for the chatbot
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SatyaVardhanM/automated-quad-machine.git
cd automated-quad-machine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add registered face images
```bash
# Add JPG/PNG images named after the user
cp your_photo.jpg faces/satya.jpg
```

### 4. Add a knowledge base
```bash
# Add any text file as chatbot.txt — the drone will use it to answer questions
echo "Your knowledge base content here" > chatbot.txt
```

### 5. Run in simulation (ArduPilot SITL)
```bash
# Start ArduPilot SITL first
sim_vehicle.py -v ArduCopter --console --map

# Then run the mission
python src/main.py 127.0.0.1:14550
```

### 6. Run on real hardware (Raspberry Pi)
```bash
# Connect via telemetry radio or USB
python src/main.py /dev/ttyUSB0
```

---

## 📸 Simulation Screenshots

The following screenshots were captured during actual ArduPilot SITL testing:

**Chatbot working (voice conversation confirmed):**
Terminal output shows:
```
Speaking...
Hi! My name is Dummy.
Recording
Finished recording
You: hi there
Dummy: I am glad you are talking to me
Recording
Finished recording
You: bye
Dummy: Bye! Take care..
```

**Drone reaching triggered GPS location:**
```
Taking off!
Altitude: 20.0
Reached target altitude
Set default/target airspeed to 3
Going towards first point for 30 seconds...
Close vehicle object
Detecting Face(s)
satya
satya: hi
Dummy: Recording
Finished recording
satya: thank you
Dummy: Returning to Launch
```

---

## 🔭 Future Enhancements

- [ ] Improved obstacle detection and avoidance during flight
- [ ] Real SMS/phone alert integration (Twilio API)
- [ ] Thermal imaging for night-time operations
- [ ] Multi-user registration support
- [ ] Mobile app for real-time monitoring
- [ ] Edge ML inference on Raspberry Pi (TFLite)

---

## 📄 Project Report

Full technical documentation including system architecture, UML diagrams, NLP algorithms, clustering analysis, and hardware specifications available in `/docs/`.

---

## 👤 Author

**M. Satyavardhan**
B.Tech Computer Science & Engineering
Malla Reddy College of Engineering, Hyderabad (JNTUH) — 2020

*Currently pursuing M.S. Computer Information Systems (AI Concentration)*
*Indiana Wesleyan University, USA*

📧 satyavardhanmudiganti@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/satya-mudiganti) | [GitHub](https://github.com/SatyaVardhanM)

---

## 🙏 Acknowledgements

Guided by **Mr. P. Sandeep**, M.Tech, Assistant Professor, Dept. of CSE, Malla Reddy College of Engineering.

---

*Built with no budget, no hardware, and 30 days to learn machine learning — because sometimes necessity is the best teacher.*
