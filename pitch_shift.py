# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:23:02 2022

@author: JonLD
"""
import numpy as np
import pydub_implementation as pdimp
import matplotlib.pyplot as plt


def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    print("speeding")
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( int(len(sound_array) / f * window_size))

    for i in np.arange(0, len(sound_array)-(window_size+h), int(h*f)):
    #for i in np.arange(0, 10000, int(h*f)):
        # two potentially overlapping subarrays
        
        a1 = sound_array[i: i + window_size]

        a2 = sound_array[i + h: i + window_size + h]
        
        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1) 
    
        
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(abs(s2)*np.exp(1j*phase))
        
        
        
        # add to result
        i2 = int(i/f)
        
        # a = result[i2 : i2 + window_size]
        #  b = hanning_window*a2_rephased
        # result[i2 : i2 + window_size] = result[i2 : i2 + window_size] + np.add(result[i2 : i2 + window_size], b, out=a, casting="unsafe")
        
        result[i2 : i2 + window_size] += abs(hanning_window*a2_rephased)
        # pdimp.plot_sample(result, 'a2')
        
        # N = 16384
        # # sample spacing
        # T = 1.0 / 48000.0
        # yf = result
        # xf = np.fft.fftfreq(N, T)[:N//2]
        
        # plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        # plt.grid()
        # plt.show()
        
    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)
    print("out of for")
    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

mysound = pdimp.pydub_audio("SineTone.wav", "TestOut.wav")
array = mysound.audio_array[0]
array = np.trim_zeros(array)

pdimp.plot_sample(np.fft.fft(array), 'a2')

shifted_array = pitchshift(array, 5)
shifted_array.reshape(sound.channels, -1, order='F');
mysound.audio_array[0] = shifted_array
mysound.audio_array[1] = shifted_array
mysound.export_audio(audio_type = "array")

