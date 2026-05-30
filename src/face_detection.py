"""
Face Detection and Identification Module
Automated Quad Machine — AI Safety Companion Drone
Author: M. Satyavardhan | B.Tech CSE, Malla Reddy College of Engineering (2020)

Detects and identifies registered users in real time via the drone-mounted
camera feed using face_recognition (dlib) and OpenCV Haar Cascades.
On a match  → chatbot initialises for that user.
On no match → drone triggers emergency alert / deploy signal.
"""

import face_recognition as fr
import os
import cv2
import numpy as np


def get_encoded_faces():
    """
    Walk the ./faces directory and encode all registered face images.
    Returns:
        dict: {name (str): face_encoding (np.ndarray)}
    """
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded


def classify_face():
    """
    Open the camera, detect all faces in the live feed, and return
    the registered user's name if found, else return 0.

    Returns:
        str | int: Recognised user name, or 0 if unrecognised.
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    video = cv2.VideoCapture(0)
    admin = 'satya'
    face_names = []

    print("Detecting Face(s)")

    while True:
        ret, img = video.read()
        face_locations = fr.face_locations(img)
        unknown_face_encodings = fr.face_encodings(img, face_locations)

        for face_encoding in unknown_face_encodings:
            matches = fr.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if name not in face_names:
                face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)
            cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left - 20, bottom + 15), font, 0.5, (255, 255, 255), 2)

        for nams in face_names:
            print(nams)
            if nams.lower() == admin.lower():
                video.release()
                cv2.destroyAllWindows()
                return admin

        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return 0
