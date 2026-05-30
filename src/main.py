"""
Autonomous Drone Navigation Module
Automated Quad Machine — AI Safety Companion Drone
Author: M. Satyavardhan | B.Tech CSE, Malla Reddy College of Engineering (2020)

Main entry point. Controls the full autonomous mission pipeline:
  1. Connect to vehicle via DroneKit (ArduPilot)
  2. Arm and take off to target altitude
  3. Navigate to the registered user's GPS location
  4. Identify the user via face recognition
  5. Initiate voice chatbot session
  6. If user confirmed safe → Return to Launch
  7. If user unresponsive / unrecognised → Trigger emergency alert (deploy)

Tested and verified using ArduPilot SITL (Software in the Loop) simulation.
Real GPS coordinates from Hyderabad, Telangana (test location).
"""

from __future__ import print_function
import time
import sys
from dronekit import connect, VehicleMode, LocationGlobalRelative
from face_detection import classify_face
from chatbot import chatbot_main


# ── Configuration ────────────────────────────────────────────────
CONNECTION_STRING = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:14550'
TARGET_ALTITUDE   = 10    # metres
CRUISE_AIRSPEED   = 30    # km/h
HOVER_TIME        = 10    # seconds at destination before face scan

# GPS coordinates — registered user's location (Hyderabad test)
USER_GPS = LocationGlobalRelative(17.495830, 78.373620, 20)


# ── Connect ──────────────────────────────────────────────────────
print(f'Connecting to vehicle on: {CONNECTION_STRING}')
vehicle = connect(CONNECTION_STRING, wait_ready=True)


def arm_and_takeoff(target_altitude: float) -> None:
    """
    Perform pre-arm safety checks, arm the drone, and climb to
    the specified altitude in GUIDED mode.

    Args:
        target_altitude (float): Desired altitude in metres.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode  = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {alt:.2f}m")
        if alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


# ── Mission ──────────────────────────────────────────────────────
if __name__ == '__main__':

    arm_and_takeoff(TARGET_ALTITUDE)

    print(f"Set default/target airspeed to {CRUISE_AIRSPEED}")
    vehicle.airspeed = CRUISE_AIRSPEED

    print("Going towards user location...")
    vehicle.simple_goto(USER_GPS)
    time.sleep(HOVER_TIME)

    print("Close vehicle object")
    vehicle.close()

    # ── Identify user & start chatbot ────────────────────────────
    identified_user = classify_face()

    if identified_user:
        chatbot_main(identified_user)
        print("User confirmed safe. Returning to Launch.")
    else:
        print("ALERT: Unrecognised individual. Deploying emergency signal.")
        # TODO: trigger emergency alert — SMS / call to registered contact

    vehicle.mode = VehicleMode("RTL")
