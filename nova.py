import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import speech_recognition as sr
import datetime

opts = {
    "alias": ('nova',),
    "tbr": ('say', 'tell', 'show', 'how match', 'run', 'play'),
    "cmds": {
        "ctime": ('tell time', 'say time', 'show time'),
        "radio": ('run music', 'tell music', 'play music'),

    }
}

# func


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="en-EN").lower()
        print("[log] recognized: " + voice)

        if voice.startwith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            cmd = recognizer_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        print("voice is`nt recognized")
    except sr.RequestError:
        print("[log] unknown error")


def recognizer_cmd(cmd):
    rc = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc


def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Now " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        os.system("vlc /media/alex/Data/audioFiles/rammstein_engel.mp3")
    else:
        print('unknown command')


# tun

r = sr.Recognizer()
m = sr.Microphone(device_index=0)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voices', voices)


speak("Hello creator")


stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
