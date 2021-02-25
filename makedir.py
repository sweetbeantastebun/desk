import os

dir = "/home/pi/Documents/admp441_data/"
dir_out = os.path.join(*[dir, "spectrogram"])
if os.path.exists(dir_out) == 0:
   os.mkdir(dir_out)
