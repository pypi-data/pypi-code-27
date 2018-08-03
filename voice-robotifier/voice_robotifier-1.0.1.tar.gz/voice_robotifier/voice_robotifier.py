import speech_recognition as sr
from .sapi import Sapi
from io import BytesIO
import time
import os
import pyaudio
import keyboard
import threading
from time import sleep
import numbers

class VoiceRobotifier:

    def __init__(self):
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.voice = Sapi()

    def set_input_device(self,device_name):
        device_id = None
        for i,name in enumerate(self.list_device_names()):
            if name == device_name[:31]:
                device_id = i
                break
        if not device_id:
            raise Exception('Device name "%s" not found' % device_input)
        self.microphone = sr.Microphone(device_id)
            

    def set_output_device(self,device_name):
        self.voice.set_audio_output(device_name)

    def list_device_names(self):
        audio = pyaudio.PyAudio()
        out = list()
        for i in range(0,audio.get_device_count()):
            out.append(audio.get_device_info_by_index(i)['name'])
        return out

    def set_voice(self,voice_name):
        self.voice.set_voice(voice_name)

    def list_voices(self):
        return self.voice.get_voice_names()

    def set_voice_rate(self,voice_rate):
        self.voice.set_rate(voice_rate)
        

    def start(self,key,key_quit='esc',block=True):
        running = Event()
        lock = Event()

        def stop():
            nonlocal lock, running
            lock.stop()
            running.set()
            keyboard.unhook(key_quit)
            print('Stopped VoiceRobotifier')

        def target():
            while not running.is_set():
                lock.clear()
                keyboard.on_press_key(key, lambda e: lock.set())

                lock.wait()
                keyboard.unhook(key)

                lock.clear()
                if running.is_set():
                    break
                keyboard.on_release_key(key, lambda e: lock.set())
                
                print('Listening...', end=' ')
                frames = BytesIO()
                with self.microphone as source:
                    while not lock.is_set():  # loop for the total number of chunks needed
                        if source.stream is None or source.stream.pyaudio_stream.is_stopped(): break
                        buffer = source.stream.read(source.CHUNK)
                        if len(buffer) == 0: break
                        frames.write(buffer)
                    keyboard.unhook(key)
                    
                    frame_data = frames.getvalue()
                    frames.close()
                    audio = sr.AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                self.__audio_to_tts(audio)

        if key_quit is not None:
            keyboard.on_press_key(key_quit,lambda e: stop())

        thread = threading.Thread(target=target,daemon=True)
        thread.start()
        print('Started VoiceRobotifier with push-to-talk key \''+str(key)+'\'')

        if block:
            thread.join()
        
        return stop


    def start_autodetect(self,energy_threshold=None,key_quit='esc',block=True):
        blocking = Event()
        
        if energy_threshold is None:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        else:
            self.recognizer.energy_threshold = energy_threshold

        def callback(recognizer,audio):
            self.__audio_to_tts(audio)
            print('Listening...', end=' ')

        print('Started VoiceRobotifier with energy threshold '+str(self.recognizer.energy_threshold))
        print('Listening...', end=' ')
        stop_listener = self.recognizer.listen_in_background(self.microphone, callback)

        def stop():
            nonlocal blocking
            stop_listener()
            blocking.set()
            keyboard.unhook(key_quit)
            print('Stopped VoiceRobotifier')
        
        if key_quit is not None:
            keyboard.on_press_key(key_quit,lambda e: stop())
        
        if block:
            blocking.wait()
        
        return stop


    def __audio_to_tts(self,audio):
        try:
            text = uncensor(self.recognizer.recognize_google(audio))
            print('"%s"' % text)
            speak_thread = threading.Thread(target=lambda: self.voice.say(text))
            speak_thread.start()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


class Event(threading.Event):
    def __init__(self):
        self.__stopped = False
        super().__init__()
    def wait(self):
        while True:
            if super().wait(0.5) or self.__stopped:
                break
    def is_set(self):
        if self.__stopped:
            return True
        return super().is_set()
    isSet = is_set
    def stop(self):
        self.__stopped = True
         
def uncensor(text):
    censored = {
        'f***': 'fuck',
        's***': 'shit',
        'b****': 'bitch',
        'a**': 'ass'
    }
    for key,val in censored.items():
        text = text.replace(key,val)
    return text

