import os
import time
import subprocess
import speech_recognition as spr
import pyttsx3
import queue
import json
import sys
from vosk import Model, KaldiRecognizer
import sounddevice as sd
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
call_to_stop = 1
#setting for using speech_recognition
current_dir = os.path.dirname(os.path.abspath(__file__))
flac_path = resource_path(os.path.join(current_dir, "flac.exe"))
spr.audio.get_flac_converter = lambda: flac_path
#setting for using vosk
model_path = resource_path(os.path.join(current_dir, 'model'))
model = Model(model_path)
#ini queue
q = queue.Queue()
#support variable
is_begin = True
is_start = 0
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
#mic ini
robot_ear = spr.Recognizer()
robot_ear.pause_threshold = 0.5
mic = spr.Microphone()
with mic:
    robot_ear.adjust_for_ambient_noise(mic, duration=0.8)
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
            speak("your command is wrong, try again")
            print("Error:\n", result.stderr)
    except Exception as e:
        speak("your command is wrong")
        print(f"Error: {e}")
#robot brain
def running_robot(command_list):
        global is_begin
        with mic:
            audio = robot_ear.listen(mic)
        try:
            text = robot_ear.recognize_google(audio,language="vi-VN").lower()
            print(f"you say: '{text}'")
            if not command_list:
                speak("your command list is blank, add commands first")
                return True
            else:
                is_flag = True
                for command in command_list:
                    if command in text:
                        run_powershell(command_list[command])
                        speak("successfully")
                        is_flag = False
                        is_begin = True
                        break
                if is_flag:
                    speak("I don't understand your command, " \
                    "please try again or checking list of command or pronunciation")
                    is_begin = True
        except spr.UnknownValueError:
            speak("I can't hear, please try again")
        except spr.RequestError as e:
            print(f"Error to connect API: {e}")
def running_backend(listofcommand,
                    opening_command = "waking up",
                    exiting_command = "stop right now"):
    global is_begin
    global is_running
    global is_start
    rec = KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=audio_callback):
        while True:
            if is_begin:
                speak(f"Hello, I'm here to help you, I'm your assistant, say {opening_command} to begin or {exiting_command} to stop")
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
                if running_robot(command_list= listofcommand):
                    break
                rec = KaldiRecognizer(model, 16000) 
                with q.mutex:
                    q.queue.clear()
            elif exiting_command in text_detected or call_to_stop:
                is_start = 1
                print('thank you')
                speak("thank you")
                break