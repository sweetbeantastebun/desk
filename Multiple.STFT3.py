#coding:utf-8
"""
オーディオファイルを読み込み
短時間フーリエ変換(stft)を変数で実行
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

def Data_Load():
    #global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global spectrum_A
    global frequency_A
    global file_list
    global freqs
    global times
    global Sx
    global t10
    t10 = time.time()
    file_list = glob.glob(path + "*.wav")
    for file in file_list:
        #os.remove(file)
        #wavfile_A = path + filename_A + ".wav"
        wr = wave.open(file, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
        fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
        samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
        samples_N = np.frombuffer(samples, dtype="int16") 
        samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
        wr.close()  #読み込み終了。ファイルオブジェクトの終了。
        #samplesを変数audio_signalとしてコピー
        audio_signal_A = samples.copy()
        #RMS
        rms_A = np.sqrt((audio_signal_A**2).mean())
        print("RMS", round(rms_A,4))
        if rms_A is np.nan:
            pass
        else:
            #FFT
            N = 8192  #サンプル数を指定 #録音10秒で4096データの周波数分解能は10Hz #8192=5Hz
            spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
            frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #周波数軸の計算
            #spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
            #frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
            #フィルタリング機能
            spectrum_A[(spectrum_A < noise_reduction_filters)] = 0  #しきい値未満の振幅はゼロにする
            #グラフ準備
            spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
            frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
            t11 = time.time()
            #print("Data_Load", t11-t10)
            #file =  filename_A + ".wav"
            #shutil.copy(path + file , path2)  #wavファイルをコピーして指定ディレクトリへ移動
            #os.remove(file)
            """STFT"""
            #フレーム数の指定
            NN = 8192
            #周波数、時間軸、スペクトル強度を算出する
            freqs, times, Sx = signal.spectrogram(samples_N, fs = fs_A, window = "hanning",
                                                  nperseg = NN,
                                                  noverlap = NN/8,
                                                  detrend = False, scaling = "spectrum") #スペクトログラム変数
    t11 = time.time()

"""
def Data_Saving():
    for i in range(len(file_list)):
        png_file = os.path.basename(file_list[i])
        name, ext = os.path.splitext(png_file)
        ext = ".png"
        out_path = os.path.join(*[path, name + ext])
    
        plt.savefig(out_path)
"""
            
def Graph_A1():
    global fig1
    global t20
    global t21
    global RMS_data
    global sample_of_numbers
    t20 = time.time()
    #グラフ作成
    """
    plt.ion()
    plt.clf()
    fig1 = plt.figure(1)
    plt.cla()
    plt.subplot(2, 1, 1)
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    #No1.set_data(sample_of_numbers, RMS_data)
    #plt.xlim(sample_of_numbers[-Loop_count_Value1], sample_of_numbers[-1])
    #plt.ylim(0, 0.06)
    plt.ylim(0, 0.05)
    #print("RMS_data", RMS_data)
    #print("RMS_data", len(RMS_data))
    #print("index_loop", index_loop)
    """
    """
    #plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.grid(which="both")
    """
    plt.pcolormesh(times, freqs, np.log10(Sx), cmap='jet', vmin=vmin, vmax=vmax)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.ylim([0, fs_A/2])
    plt.ylabel("Frequency[Hz]", fontsize=8)
    plt.xlabel("Time[sec]", fontsize=8)
    plt.colorbar(aspect=40, pad=0.02)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    for i in range(len(file_list)):
        png_file = os.path.basename(file_list[i])
        name, ext = os.path.splitext(png_file)
        ext = ".png"
        out_path = os.path.join(*[path, name + ext])
    
        plt.savefig(out_path)
        #print(str(i+1) + "done!")
    t21 = time.time()
    #plt.savefig("/home/pi/Documents/admp441_data/"+"Maximum_Value"".png")
    #fig1.savefig("/home/pi/Documents/admp441_data/"+filename_A+"Maximum_Value"".png")
    #plt.draw()

   
Data_Load()
#Graph_A1()
#print("time", t21-t10)
"""
while True:
    Data_Load()
    Graph_A1()
    print("time", t21-t10)
"""
