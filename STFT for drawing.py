#coding:utf-8
"""
ディレクトリ内の複数wavファイルをまとめて処理
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
Loop_count_Value1 = 5
Loop_count_Value2 = 10
#しきい値を指定
threshold_value_MAX = 0.13
threshold_value_MIN = 0.005
#FFT検出強度のフィルタリング
noise_reduction_filters = 0
#カラーバーのレンジ指定
vmin = -300
vmax = 200

t00 = time.time()
path = "/home/pi/Documents/admp441_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path2 ="/home/pi/Documents/admp441_data/Save_wavfile"

def Drawing():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second) + "." + str(timestamp.microsecond)
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
    File_List = glob.glob(path + "*.wav")
    for audiofile in File_List:
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
        """RMS"""
        rms_A = np.sqrt((audio_signal_A**2).mean())
        if rms_A is np.nan:
            pass
        else:
            #print("RMS", round(rms_A,4))
            t4= time.time()
            """FFT"""
            N = 8192  #サンプル数を指定 #録音10秒で4096データの周波数分解能は10Hz #8192=5Hz
            spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
            frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #周波数軸の計算
            #フィルタリング機能
            spectrum_A[(spectrum_A < noise_reduction_filters)] = 0  #しきい値未満の振幅はゼロにする
            #グラフ準備
            spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
            frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
            t5 = time.time()
            #print("Recording_A", t5-t0)
            """STFT"""
            #フレーム数の指定
            NN = 8192
            #周波数、時間軸、スペクトル強度を算出する
            freqs, times, Sx = signal.spectrogram(samples_N, fs = fs_A, window = "hanning",
                                                  nperseg = NN,  #nperseg:分割数
                                                  noverlap = NN/8,  #フレームの重なり具合。
                                                  detrend = False, scaling = "spectrum") # スペクトログラム変数
            t6 = time.time()
            print("signal_spectrogram", t6-t5)
        
            #グラフ作成
            #FullScall
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            """
            #plt.ylim([0, 1000])
            plt.ylim([0, framerate/2])
            plt.ylabel("Frequency[Hz]", fontsize=10)
            plt.xlabel("Time[s]", fontsize=10)
            plt.xticks(fontsize = 9)
            plt.yticks(fontsize = 9)
            plt.colorbar(aspect=40, pad=0.02).set_label("SP[Pa]", fontsize=9)
            """
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name + ext])
            plt.saefig(out_path)
            plt.close()
            t8 = time.time()
            
            #4000Hz
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name+"_4000Hz" + ext])
            plt.saefig(out_path)
            plt.close()
            t9 = time.time()
            
            #8000Hz
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name+"_8000Hz" + ext])
            plt.saefig(out_path)
            plt.close()
            t10 = time.time()
            
            #12000Hz
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name+"_12000Hz" + ext])
            plt.saefig(out_path)
            plt.close()
            t11 = time.time()
            
            #16000Hz
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name+"_16000Hz" + ext])
            plt.saefig(out_path)
            plt.close()
            t12 = time.time()
            
            #20000Hz
            plt.pcolormesh(times, freqs, 10* np.log(Sx), cmap='jet', vmin=vmin, vmax=vmax, shading="gouraud")
            plt.ylim([0, 4000])
            #軸ラベル表示無しにするコマンド
            plt.xticks([])
            plt.yticks([])
            #グラフ余白なしにするコマンド
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            name, ext = os.path.splitext(audiofile)
            ext = ".png"
            out_path = os.path.join(*[path, name+"_20000Hz" + ext])
            plt.saefig(out_path)
            plt.close()
            t13 = time.time()


#except KeyboardInterrupt:
#print("FINISH!")
