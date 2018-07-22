from .settings import get_argument_parser, get_settings
from .irloader import IRLoader
import sounddevice

def main():

    args = get_argument_parser()

    if 'help' in args:
        return

    settings = get_settings(args)

    irloader = IRLoader(
        ir=settings.ir_file,
        source=settings.looper_file if settings.looper else '',
        target='',
        looper=settings.looper
    )

    #irloader = IRLoader(
        #ir="data/Engl 412 St 2a.wav",
        #ir="data/Engl 412 St 2b.wav",
        #ir="data/Marshall Heritage G12H 2a.wav",
        #ir="data/TN Mar412-V30 Blend 1.wav",
        #source="data/src.wav", target="data/target.wav")
        #ir="data/Greek 7 Echo Hall.wav", source="data/target.wav", target="data/target_w_reverb.wav")
        #source="data/src.wav", target="", looper=True)

    irloader.read()
    irloader.process()
    
    if settings.looper:
        irloader.looper()
    else:
        irloader.play()
