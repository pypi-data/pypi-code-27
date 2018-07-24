#!/usr/bin/env python3
import os
import sys

from tongue.output_control import OutputControl
from peak_bot import PeakBot

def main():
    '''
    Sets the verbosity in respect to the user input.
    Checks if settings are good.
    Instantiate a peak-bot.
    '''
    supported_platforms = ('windows', 'linux')
    if sys.platform not in supported_platforms:
        oc.print(oc.PLAT_NOT_SUP, sys.platform) 
        sys.exit()

    verbosity = 0
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            verbosity = sys.argv[1]

    oc = OutputControl(range(0, 8), str(verbosity))
    oc.print(oc.WELCOME_MSG) 
    settings_path = "peak_data/configuration/settings.json"
    audio_base_path = "peak_data/configuration/audio_base.json"
    lang_base_path = "peak_data/configuration/lang_base.json"
    library_path = "peak_data/library/"
    audio_wav_path = "brain/fs_memory/.temp_recording.wav"
    fundamental_directories = (settings_path, audio_base_path, lang_base_path, library_path, audio_wav_path)
    bot = PeakBot(fundamental_directories, oc)
        
if __name__ == '__main__':
    main()
