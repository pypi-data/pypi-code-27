import micral_grain_core
import micral_harmonic_core
import micral_utils

def globalAnalyseCore(images):
    dict_output = dict()
    
    dict_grain = micral_grain_core.analyse(images)
    dict_harmonic = micral_harmonic_core.analyse(images)
    
    for image in images:
        dict_output[image] = dict()
        if image in dict_grain:
            dict_output[image]['grain'] = dict_grain[image]
        if image in dict_harmonic:
            dict_output[image]['harmonic'] = dict_harmonic[image]
    
    return micral_utils.removeEmptyDict(dict_output)