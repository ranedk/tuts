import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image
img = Image.open('../data/iss.jpg')
imgarray = np.asarray(img) # imgarray.shape will be width x height x channels


from scipy.io import wavfile
rate, snd = wavfile.read(filename='../data/sms.wav')
# rate tells you the frequency of data collection or play
# 44.1 kHz means 44100 times per second. So a 3-second file contains over 100k samples,
# with each second, we have 44100 sample of sound frequencies

from IPython.display import Audio
Audio(data=snd, rate=rate) # render wav file in audio embeded in HTML

plt.plot(snd) # Plot the snd data, which is an array of 

# Raw audio is an array of audio frequencies and isn't the best representation
# One way is to create a Spectogram out of it.
# The Spectogram is a FFT transform which shows at what time, what all frequencies were active
# The spectogram will give a colored density graph for frequency bins in a given time bin
_ = plt.specgram(snd, NFFT=1024, Fs=44100)
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.title('sms.wav as a Spectrogram');
