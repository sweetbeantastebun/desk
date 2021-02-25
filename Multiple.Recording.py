#coding:utf-8
"""
マイクから録音、オーディオファイルを読み込み
"""
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import numpy as np #行列、配列計算、FFT化するライブラリ
from scipy import signal  #信号処理や統計を使用するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import psutil  #メモリ、CPUの使用率をモニターするライブラリ

#グラフのリアルタイムプロットの更新時間数
Loop_count_Value1 = 250
Loop_count_Value2 = 1000
#しきい値を指定
threshold_value_MAX = 0.030
threshold_value_MIN = 0.015
#FFT検出強度のフィルタリング
noise_reduction_filters = 0
#カラーバーのレンジ指定
vmin = -10
vmax = 10

t00 = time.time()
path = "/home/pi/Documents/admp441_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path2 ="/home/pi/Documents/admp441_data/Save_wavfile"

def Recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second) + "." + str(timestamp.microsecond)
    #録音実行（16ビット量子化、44.1kHz）
    record = 'arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()
    #wavファイルの読み込み
    global t2
    global t3
    global t4
    global t5
    global t6
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global spectrum_A
    global frequency_A
    global freqs
    global times
    global Sx
    t2 = time.time()
    wavfile_A = path + filename_A + ".wav"
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples_N = np.frombuffer(samples, dtype="int16")
    samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    audio_data_length = np.arange(0, len(samples))/float(fs_A) # 音声データの長さ(x軸)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t3 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_A = samples.copy()
    #RMS
    rms_A = np.sqrt((audio_signal_A**2).mean())
    print("RMS", round(rms_A,4))
    t4 = time.time()
    print("Recording", t4-t0)
    """
    if rms_A is np.nan:
        pass
    else:
        #print("RMS", round(rms_A,4))
        t4= time.time()
        #FFT
        N = 8192  #繧ｵ繝ｳ繝励Ν謨ｰ繧呈欠螳� #骭ｲ髻ｳ10遘偵〒4096繝��繧ｿ縺ｮ蜻ｨ豕｢謨ｰ蛻�ｧ｣閭ｽ縺ｯ10Hz #8192=5Hz
        spectrum_A = np.fft.fft(samples[0:N])  #2谺｡蜈��蛻�(螳滄Κ�瑚劒驛ｨ)
        frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #蜻ｨ豕｢謨ｰ霆ｸ縺ｮ險育ｮ�
        #spectrum_A = np.fft.fft(samples)  #2谺｡蜈��蛻�(螳滄Κ�瑚劒驛ｨ)
        #frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #蜻ｨ豕｢謨ｰ霆ｸ縺ｮ險育ｮ�
        #繝輔ぅ繝ｫ繧ｿ繝ｪ繝ｳ繧ｰ讖溯�
        spectrum_A[(spectrum_A < noise_reduction_filters)] = 0  #縺励″縺�､譛ｪ貅縺ｮ謖ｯ蟷��繧ｼ繝ｭ縺ｫ縺吶ｋ
        #繧ｰ繝ｩ繝墓ｺ門ｙ
        spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #繧ｹ繝壹け繝医Ν縺後�繧､繝翫せ縺ｫ縺ｪ繧九せ繝壹け繝医Ν隕∫ｴ�縺ｮ蜑企勁
        frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #蜻ｨ豕｢謨ｰ縺後�繧､繝翫せ縺ｫ縺ｪ繧句捉豕｢謨ｰ隕∫ｴ�縺ｮ蜑企勁    
        t5 = time.time()
        #print("Recording_A", t5-t0)
        #STFT
        #繝輔Ξ繝ｼ繝�謨ｰ縺ｮ謖�ｮ�
        NN = 8192
        #蜻ｨ豕｢謨ｰ縲∵凾髢楢ｻｸ縲√せ繝壹け繝医Ν蠑ｷ蠎ｦ繧堤ｮ怜�縺吶ｋ
        freqs, times, Sx = signal.spectrogram(samples_N, fs = fs_A, window = "hanning",
                                              nperseg = NN,
                                              noverlap = NN/8,
                                              detrend = False, scaling = "spectrum") # 繧ｹ繝壹け繝医Ο繧ｰ繝ｩ繝�螟画焚
    """

while True:
    Recording_A()
    
#except KeyboardInterrupt:
#print("FINISH!")
