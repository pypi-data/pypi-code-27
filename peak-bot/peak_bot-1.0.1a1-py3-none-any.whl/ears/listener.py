from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave


class Listener:
    portaudio_formats = {
        'uint8':pyaudio.paUInt8,
        'int8' :pyaudio.paInt8,
        'int16':pyaudio.paInt16,
        'int24':pyaudio.paInt24,
        'int32':pyaudio.paInt32,
        'float32':pyaudio.paFloat32
        }

    def set_values(self, audio_settings_dict):
        for audio_values in audio_settings_dict['audio_values']:
            if audio_values['active'] == 'True':
                self.format = self.portaudio_formats[audio_values['format']]
                self.threshold = int(audio_values['threshold'])
                self.sample_rate = int(audio_values['rate'])
                self.chunk_size = int(audio_values['chunk_size'])
                self.max_volume = int(audio_values['max_volume'])

    def listen(self):
        py_audio = pyaudio.PyAudio()
        py_stream = py_audio.open(format=self.format, channels=1, rate=self.sample_rate, input=True, output=True, frames_per_buffer=self.chunk_size)
        silent_time = 0
        voice_started = False
        audio_data = array('h')

        self.output_control.print(self.output_control.EARS_READY)
        while True:
            temp_data = array('h', py_stream.read(self.chunk_size))
            if byteorder == 'big':
                temp_data.byteswap()
            audio_data.extend(temp_data)

            if not voice_started and max(temp_data) >= self.threshold:
                self.output_control.print(self.output_control.VOICE_DTC)
                voice_started = True
            if voice_started:
                if max(temp_data) < self.threshold:
                    silent_time += 1
                    if silent_time < 25:
                        self.output_control.print(self.output_control.SILENCE, (silent_time,))
                    else:
                        break
                else:
                    silent_time = 0

        sample_width = py_audio.get_sample_size(self.format)
        py_stream.stop_stream()
        py_stream.close()
        py_audio.terminate()
        multiplier = float(self.max_volume)/max(abs(piece) for piece in audio_data)
        temp_data = array('h')
        for piece in audio_data:
            temp_data.append(int(piece*multiplier))
        audio_data = temp_data
        return sample_width, audio_data 

    def record(self):
        sample_width, audio_data = self.listen()
        data = pack('<' + ('h'*len(audio_data)), *audio_data)
        wave_file = wave.open(self.file_path, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(audio_data)
        wave_file.close()

    def __init__(self, output_control, audio_settings_dict, audio_wav_path):
        self.output_control = output_control
        self.set_values(audio_settings_dict)
        self.file_path = audio_wav_path
