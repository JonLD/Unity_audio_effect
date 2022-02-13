# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:59:44 2022

@author: JonLD
"""
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize
import numpy as np
import pydub_implementation as pdimp

#unify function adds stereo information by creating multiple voices, adding slight detune and panning each voice
#max_detune is input as number of semitones change in tuning
#width is numb between 0 and 1, 1 resulting in 100% left and right pan of 
def unify(audio_segment, num_voices, max_detune, width):
    if num_voices < 2:
        print('Must have 2 or more voices')
        return
    if width < 0 or width > 1:
        print('Width must be a number between 0 and 1')
        return
    
    voice_array = [audio_segment for x in range(0,num_voices)]
        
    octave_shift = max_detune/12 # max_detune given in semitones so convert to octaves
    
    # as we start and end at min and max we must subtract 1 from num_voices when finding seperation between voices
    pan_seperation = 2*width / (num_voices-1)
    pitch_seperation = (octave_shift) / (num_voices-1)
    
    #start at the max pan to left and max negative detune 
    #move to right by pan_seperation and increase pitch by pitch_seperation for each subsequent voice
    temp_pitch = -octave_shift
    temp_pan = - width
    
    new_voice_array = []
    for v in voice_array:
        temp_v = v.pan(temp_pan)
        temp_pan += pan_seperation
        
        new_sample_rate = int(temp_v.frame_rate * (2.0 ** temp_pitch))
        shifted_v = temp_v._spawn(temp_v.raw_data, overrides={'frame_rate': new_sample_rate})
        shifted_v = shifted_v.set_frame_rate(44100)
        new_voice_array.append(shifted_v)
        temp_pitch += pitch_seperation
    
    sound_length = len(audio_segment)
    combined_audio = AudioSegment.silent(duration = sound_length)  
    
    for x in new_voice_array:
        combined_audio = combined_audio.overlay(x)
    
    original_peak_amplitiude = audio_segment.max_dBFS
    new_peak_amplitiude = combined_audio.max_dBFS
    volume_dif = original_peak_amplitiude - new_peak_amplitiude
    combined_audio = combined_audio.apply_gain(volume_dif)

    return combined_audio
    
sound = pdimp.pydub_audio('OneShot_test.wav', 'unify_out.wav')   
sound.audio_segment = unify(sound.audio_segment, 5, 0.02, 1)
sound.export_audio()

