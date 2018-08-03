import speech_recognition as sr
from io import BytesIO
import time
import os
import pyaudio
import keyboard
import threading
from time import sleep
from pkg_resources import resource_filename
import tempfile
import subprocess
import wave

class VoiceRobotifier:

    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__audio = pyaudio.PyAudio()

        self.__microphone = None
        self.set_input_device(self.__audio.get_default_input_device_info()['name'])
        
        self.__output_index = None
        self.set_output_device(self.__audio.get_default_output_device_info()['name'])

        self.__dectalk = resource_filename('voice_robotifier','dectalk')

        self.__modifiers = {
            'name': 'Paul',
            'rate': 200
        }
            

    def set_input_device(self,device_name):
        self.__microphone = sr.Microphone(self.__get_device_index(device_name))

    def set_output_device(self,device_name):
        self.__output_index = self.__get_device_index(device_name)

    def list_device_names(self):
        out = list()
        for i in range(0,self.__audio.get_device_count()):
            out.append(self.__audio.get_device_info_by_index(i)['name'])
        return out

    def __get_device_index(self,device_name):
        device_index = None
        for i,name in enumerate(self.list_device_names()):
            if name == device_name[:31]:
                device_index = i
                break
        if device_index is None:
            raise Exception('Device name "{0}" not found'.format(device_name))
        return device_index

    def set_voice_name(self,voice_name):
        assert voice_name in self.list_voice_names()
        self.__modifiers['name'] = voice_name

    def list_voice_names(self):
        return ['Paul','Harry','Frank','Dennis','Betty','Ursula','Wendy','Rita','Kit']

    def set_voice_rate(self,voice_rate):
        assert type(voice_rate) is int
        self.__modifiers['rate'] = max(0, min(32767, voice_rate))

    def __modifiers_str(self):
        out = str()
        for key,val in self.__modifiers.items():
            out += '[:{0} {1}]'.format(key,val)
        return out

    def start(self,key,key_quit='esc',block=True):
        running = Event()
        lock = Event()

        def stop():
            nonlocal lock, running
            lock.stop()
            running.set()
            if keyboard.key_to_scan_codes(key) != keyboard.key_to_scan_codes(key_quit):
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
                with self.__microphone as source:
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
            with self.__microphone as source:
                self.__recognizer.adjust_for_ambient_noise(source)
        else:
            self.__recognizer.energy_threshold = energy_threshold

        def callback(recognizer,audio):
            self.__audio_to_tts(audio)
            print('Listening...', end=' ')

        print('Started VoiceRobotifier with energy threshold '+str(self.__recognizer.energy_threshold))
        print('Listening...', end=' ')
        stop_listener = self.__recognizer.listen_in_background(self.__microphone, callback)

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
            text = uncensor(self.__recognizer.recognize_google(audio))
            print('"{0}"'.format(text))

            def say(text):
                with tempfile.NamedTemporaryFile(dir=self.__dectalk, suffix='.wav') as tmpfile:
                    path = tmpfile.name
                path_name = os.path.basename(path)

                cmd = 'say.exe -w "{0}" "{1} {2}"'.format(path_name,self.__modifiers_str(),text)
                subprocess.call(cmd, cwd=self.__dectalk, shell=True)

                try:
                    with wave.open(path,'rb') as wav:
                        stream = self.__audio.open(format = self.__audio.get_format_from_width(wav.getsampwidth()),  
                            channels = wav.getnchannels(),  
                            rate = wav.getframerate(),  
                            output = True,
                            output_device_index = self.__output_index)
                        chunk = 1024
                        #read data  
                        data = wav.readframes(chunk)  

                        #play stream  
                        while data:  
                            stream.write(data)  
                            data = wav.readframes(chunk)  

                        #stop stream  
                        stream.stop_stream()
                        stream.close()
                finally:
                    os.remove(path)
            
            say_thread = threading.Thread(target=lambda: say(text))
            say_thread.start()
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

