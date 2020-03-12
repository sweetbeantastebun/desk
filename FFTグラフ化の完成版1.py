# -*- coding: utf-8 -*-
import time  #タイムカウントに使用するライブラリ
import numpy as np  #配列計算、FFT化するライブラリ
import wave     #wavファイルの読み書きするライブラリ
import pyaudio  #録音機能を使うためのライブラリ
import subprocess  #Terminalを実行するライブラリ
import csv  #csvを作成するライブラリ
from pydub import AudioSegment  #メディアデータの変換ライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil

def Recording_A():
    global t0
    global t1
    global t2
    global t3
    global t4
    global CHANNELS_A
    global RATE_A
    global p_A
    global FORMAT_A
    global str_data_A
    t0 = time.time()
    #基本情報の設定
    timestamp = datetime.today()  #現在の日付、現在の時刻、ここでは測定開始時刻
    global FileName_A
    FileName_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "-" + str(timestamp.microsecond)
    global wavFileName_A
    wavFileName_A = FileName_A + ".wav"
    #wavFileName_A = '/home/pi/Documents/admp441_data/'+FileName_A+'.wav'
    Record_Seconds = 5
    chunk = 512  #音源から1回(1/RATE毎)読み込む時のデータ点数。フレームサイズ。1024(=2**10)
    FORMAT_A = pyaudio.paInt16  #音源(=バイナリデータ)符号付き16ビット(-32768～32767)のバイナリ文字 #内訳,15ビット数字と1ビットの符号
    CHANNELS_A = 1  #モノラル。ステレオは2
    #RATE_A = 44032  #(215/5*1024)
    RATE_A = 44100  #サンプルレート,fs(個/sec),44.1kHz
    
    p_A = pyaudio.PyAudio()  #PyAudioインスタンスを作成する
    stream = p_A.open(format = FORMAT_A,  #入力用Streamを開く。
                    channels = CHANNELS_A,
                    rate = RATE_A,
                    input = True,
                    frames_per_buffer = chunk)  #frames:pythonのwaveモジュールではバイナリデータ個数
    t1 = time.time()
    #レコード開始
    #print("Now Recording...")
    all = []  #append前に空リスト作成
    for i in range(0, int(RATE_A / chunk * Record_Seconds)):  #フレームサイズ毎に音声を録音している。ループ回数を計算値となる。
        data = stream.read(chunk)  #音声を読み取る。
        all.append(data)  #データを追加
    #レコード終了
    #print("Finished Recording.")
    #print('all',len(all))
    #print(all)
    t2 = time.time()
    stream.close()  #Streamをcloseする
    p_A.terminate()  #PyAudioインスタンスを終了する    
    str_data_A = b"".join(all)  #録音したデータのバイト型配列から文字列に変換
    #print(data)
    result = np.frombuffer(str_data_A,dtype="int16") / float((np.power(2, 16) / 2) - 1) 
    #result = np.frombuffer(str_data_A,dtype="int16") / float(2**15)  #配列に変換。#-1～1に正規化のためfloat(x)xの浮動小数点数への変換. #int16:符号付き16bit(=2byte)
    #np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-result"), result, fmt='%.5f')
    t3 = time.time()
    wavFile = wave.open(wavFileName_A, "wb")
    wavFile.setnchannels(CHANNELS_A)
    wavFile.setsampwidth(p_A.get_sample_size(FORMAT_A))
    wavFile.setframerate(RATE_A)
    wavFile.writeframes(str_data_A)
    wavFile.close()
    t4 = time.time()
    
def MakeAudioFile_A():
    #global t4
    global t5
    global t6
    global t7
    global t8
    #t4 = time.time()
    #wavFile = wave.open(wavFileName_A, "wb")
    #wavFile.setnchannels(CHANNELS_A)
    #wavFile.setsampwidth(p_A.get_sample_size(FORMAT_A))
    #wavFile.setframerate(RATE_A)
    #wavFile.writeframes(str_data_A)
    #wavFile.close()
    t5 = time.time()
    #MP3に圧縮
    mpeg = 'lame -V 2 '+FileName_A+'.wav ''/home/pi/Documents/admp441_data/'+FileName_A+'.mp3'
    subprocess.call(mpeg, shell=True)
    t6 = time.time()
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+FileName_A+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())  #音声データをリストで受け取る(配列データの取り出し)
    #np.savetxt(FileName_A+"-samples", samples, fmt='%.5f')
    #print('samples',len(samples))
    t7 = time.time()
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)  #2次元配列(実部，虚部)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    spec = spec[:int(spec.shape[0]/2 + 1)]    #周波数がマイナスになるスペクトル要素の削除
    freq = freq[:int(freq.shape[0]/2 + 1)]    #周波数がマイナスになる周波数要素の削除
    #freq = np.fft.fftfreq(samples, 1.0/mp3_version.frame_rate)
    #print('samples大きさ',samples.shape)  #(220160,)
    #print('samples大きさ',len(samples.shape))  #1
    #print(type(samples.shape))  #<class 'tuple'>
    #print('samples行数',samples.shape[0])  #220160
    #print('samples列数',samples.shape[1])  #Error、Out of range.
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq, np.abs(spec))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(freq, np.abs(spec))
    plt.xlim(0, 1000)
    plt.ylim(0, 10000000)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(freq, np.abs(spec))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    plt.savefig('/home/pi/Documents/admp441_data/'+FileName_A+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+FileName_A+'.png', 'saved')
    np.savetxt('/home/pi/Documents/admp441_data/'+FileName_A+'spec', np.abs(spec), delimiter = " ", fmt='%.2f')
    np.savetxt('/home/pi/Documents/admp441_data/'+FileName_A+'freq', freq, delimiter = " ", fmt='%.2f')
    #time.sleep(3.0)
    t8 = time.time()


while True:
    Recording_A()
    MakeAudioFile_A()
    #print('Recording_A',t3-t0)
    #print('MakeAudioFile_A',t8-t4)
    print('Recording_A',t4-t0)
    print('MakeAudioFile_A',t8-t5)
    #time.sleep(1.0)




#g = np.frombuffer(g, dtype="int16") / float(2**15)
#frombuffer(x, dtype="int16")は、xを2バイト単位のデータが並んでいるバイナリデータとみなして、1次元配列にする。
#符号付2バイトなので、各要素の値は、-32768～32767 になります。

#x=frombuffer(x, dtype="int16")   #(1)
#x=x/32768                        #(2)
#と分けて書くことができます。(1)は上で説明した通りです。
#(2)は numpy では、「ndarray / 数値」で、「ndarray内の各要素を数値で割る」という処理を表現できます。
#このため -32768～32767 の値を 32768で割るため、各要素が -1以上1未満のfloat な ndarray になります。
#正規化
