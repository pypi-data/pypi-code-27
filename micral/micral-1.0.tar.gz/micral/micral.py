
import micral_grain
import micral_harmonic
import micral_utils

def globalAnalyse(images):
    output_dict = dict()
    grain = micral_grain.analyse(images)
    harmonic = micral_harmonic.analyse(images)
    for i in range(len(images)):
        if not isinstance(images[i], str):
            name = "image" + str(i)
        else:
            name = images[i]
        output_dict[name] = dict(coarse_grain=grain[i], harmonicity=harmonic[i])
    micral_utils.printDict(output_dict)
    return output_dict