import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class GoogleTranscriber:
    client = speech.SpeechClient()

    def transcribe(self, audio_path):
        file_name = os.path.join(os.path.curdir, audio_path)
        self.output_control.print(self.output_control.TRANSC, (audio_path,))
        with io.open(file_name, 'rb') as audio_file:
            audio = types.RecognitionAudio(content=audio_file.read())
        response = self.client.recognize(self.config, audio)
        return response.results[0].alternatives

    def __init__(self, output_control, audio_settings_dict, expected_calls):
        self.output_control = output_control
        for audio_values in audio_settings_dict['audio_values']:
            if audio_values['active'] == 'True':
                self.config = types.RecognitionConfig(
                    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz = int(audio_values['rate']),
                    language_code = audio_values['language'],
                    max_alternatives = int(audio_values['max_alternatives']),
                    speech_contexts = [{ "phrases": expected_calls}]
                    )
