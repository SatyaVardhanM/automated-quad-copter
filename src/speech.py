"""
Speech-to-Text and Text-to-Speech Module
Automated Quad Machine — AI Safety Companion Drone
Author: M. Satyavardhan | B.Tech CSE, Malla Reddy College of Engineering (2020)

Handles all audio I/O for the drone:
  - play_aud()  : converts text → speech and plays it via the drone speaker
  - aud_rec()   : records from the onboard mic and returns recognised text
"""

import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import os
import pyaudio
import wave


def play_aud(text: str) -> None:
    """
    Convert a text string to speech using Google TTS and play it.

    Args:
        text (str): The text the drone should speak aloud.
    """
    tts = gTTS(text)
    tts.save('output.mp3')
    playsound('output.mp3')
    os.remove('output.mp3')


def aud_rec() -> str:
    """
    Record 6 seconds of audio from the onboard microphone,
    save as WAV, and return the recognised text via Google Speech API.

    Returns:
        str: Transcribed speech text.
    """
    CHUNK = 1024
    SAMPLE_FORMAT = pyaudio.paInt32
    CHANNELS = 2
    RATE = 44100
    SECONDS = 6
    FILENAME = "output.wav"

    p = pyaudio.PyAudio()
    print('Recording')

    stream = p.open(
        format=SAMPLE_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        frames_per_buffer=CHUNK,
        input=True
    )

    frames = []
    for _ in range(0, int(RATE / CHUNK * SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Finished recording')

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    r = sr.Recognizer()
    with sr.AudioFile(FILENAME) as source:
        audio = r.record(source, duration=10)

    return r.recognize_google(audio)
