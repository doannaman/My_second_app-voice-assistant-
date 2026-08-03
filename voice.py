import os
import time
import subprocess
import speech_recognition as spr
import pyttsx3
import queue
import json
from vosk import Model, KaldiRecognizer
import sounddevice as sd
#setting for using speech_recognition
current_dir = os.path.dirname(os.path.abspath(__file__))
flac_path = os.path.join(current_dir, "flac.exe")
spr.audio.get_flac_converter = lambda: flac_path
#setting for using vosk
model_path = os.path.join(current_dir, 'model')
model = Model(model_path)
#ini queue
q = queue.Queue()
#support variable
is_begin = True
#listening in queue
def audio_callback(data, frames, time, status):
    q.put(bytes(data))
# robot speaking
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        new_engine = pyttsx3.init()
        new_engine.say(text)
        new_engine.runAndWait()
#writing code into the powershell
def run_powershell(command):
    try:
        print(f"Executing PowerShell command: {command}")
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.stdout:
            print("Output:\n", result.stdout)
        if result.stderr:
            speak("your command is wrong")
            print("Error:\n", result.stderr)
    except Exception as e:
        speak("your command is wrong")
        print(f"Error: {e}")
#robot brain
def running_robot():
        global is_begin
        robot_ear = spr.Recognizer()
        with spr.Microphone() as mic:
            robot_ear.adjust_for_ambient_noise(mic, duration=0.5)
            audio = robot_ear.listen(mic)
        try:
            text = robot_ear.recognize_google(audio).lower()
            print(f"you say: '{text}'")
            if "start chrome" in text:
                run_powershell("Start-Process chrome")
                speak("successfully")
            elif "start notepad" in text:
                run_powershell("notepad")
            elif "start word" in text:
                run_powershell("Start-Process winword")
                speak("successfully")
            elif "start excel" in text:
                run_powershell("start excel")
                speak("successfully")
            elif "turn off the computer" in text:
                run_powershell('shutdown /s /t 0')
                speak("successfully")
            else:
                speak("I don't understand your command, please try again or checking list of command or pronunciation")
            is_begin = True
        except spr.UnknownValueError:
            speak("I can't hear, please try again")
        except spr.RequestError as e:
            print(f"Error to connect API: {e}")
def running_backend(opening_command = "waking up",
                    exiting_command = "stop right now"):
    global is_begin
    rec = KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=audio_callback):
        while True:
            if is_begin:
                speak(f"Hello, I'm here to help you, I'm your assistant, say {opening_command} to begin")
                is_begin = False
                rec.Reset()
                with q.mutex:
                    q.queue.clear()
            print("Robot is hearing")
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text_detected = result.get("text", "")
            else:
                partial_result = json.loads(rec.PartialResult())
                text_detected = partial_result.get("partial", "")
            if opening_command in text_detected:
                print("I'm ready to help you")
                speak("I am ready to help you")
                time.sleep(1)
                running_robot()
                rec = KaldiRecognizer(model, 16000) 
                with q.mutex:
                    q.queue.clear()
            elif exiting_command in text_detected:
                print('thank you')
                speak("thank you")
                break