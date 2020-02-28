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
    Record_Seconds = 5
    chunk = 1024  #音源から1回(1/RATE毎)読み込む時のデータ点数。1024(=2**10)
    FORMAT_A = pyaudio.paInt16  #音源(=バイナリデータ)符号付き16ビット(-32768～32767)のバイナリ文字 #内訳,15ビット数字と1ビットの符号
    CHANNELS_A = 1  #モノラル。ステレオは2
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
    for i in range(0, int(RATE_A / chunk * Record_Seconds)):  #整数化。RATEをChunkで割り切れる数に合わせる。
        data = stream.read(chunk)  #音声を読み取る。
        all.append(data)  #データを追加
    #レコード終了
    #print("Finished Recording.")
    #print(data)
    t2 = time.time()
    stream.close()  #Streamをcloseする
    p_A.terminate()  #PyAudioインスタンスを終了する    
    str_data_A = b"".join(all)  #録音したデータのバイト型配列から文字列に変換
    #print(data)
    result = np.frombuffer(str_data_A,dtype="int16") / float(2**15)  #-1～1に正規化のためfloat(x)xの浮動小数点数への変換. #int16:符号付き16bit(=2byte)
    #np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-result"), result, fmt='%.5f')
    t3 = time.time()
    
def MakeAudioFile_A():
    global t4
    global t5
    global t6
    global t7
    global t8
    t4 = time.time()
    wavFile = wave.open(wavFileName_A, "wb")
    wavFile.setnchannels(CHANNELS_A)
    wavFile.setsampwidth(p_A.get_sample_size(FORMAT_A))
    wavFile.setframerate(RATE_A)
    wavFile.writeframes(str_data_A)
    wavFile.close()
    t5 = time.time()
    #MP3に圧縮
    mpeg = 'lame -V 2 '+FileName_A+'.wav ''/home/pi/Documents/admp441_data/'+FileName_A+'.mp3'
    subprocess.call(mpeg, shell=True)
    t6 = time.time()
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+FileName_A+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())
    t7 = time.time()
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    #ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq, np.abs(spec))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(freq, np.abs(spec))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("FFT", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(freq, np.abs(spec))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.show()
    plt.savefig('/home/pi/Documents/admp441_data/'+FileName_A+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+FileName_A+'.png', 'saved')
    t8 = time.time()

def Recording_B():
    global t9
    global t10
    global t11
    global t12
    global CHANNELS_B
    global RATE_B
    global p_B
    global FORMAT_B
    global str_data_B
    t9 = time.time()
    #基本情報の設定
    timestamp = datetime.today()  #現在の日付、現在の時刻、ここでは測定開始時刻
    global FileName_B
    FileName_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "-" + str(timestamp.microsecond)
    global wavFileName_B
    wavFileName_B = FileName_B + ".wav"
    Record_Seconds = 5
    chunk = 1024  #音源から1回(1/RATE毎)読み込む時のデータ点数。1024(=2**10)
    FORMAT_B = pyaudio.paInt16  #音源(=バイナリデータ)符号付き16ビット(-32768～32767)のバイナリ文字 #内訳,15ビット数字と1ビットの符号
    CHANNELS_B = 1  #モノラル。ステレオは2
    RATE_B = 44100  #サンプルレート,fs(個/sec),44.1kHz
    
    p_B = pyaudio.PyAudio()  #PyAudioインスタンスを作成する
    stream = p_B.open(format = FORMAT_B,  #入力用Streamを開く。
                    channels = CHANNELS_B,
                    rate = RATE_B,
                    input = True,
                    frames_per_buffer = chunk)  #frames:pythonのwaveモジュールではバイナリデータ個数
    t10 = time.time()
    #レコード開始
    #print("Now Recording...")
    all = []  #append前に空リスト作成
    for i in range(0, int(RATE_B / chunk * Record_Seconds)):  #整数化。RATEをChunkで割り切れる数に合わせる。
        data = stream.read(chunk)  #音声を読み取る。
        all.append(data)  #データを追加
    #レコード終了
    #print("Finished Recording.")
    #print(data)
    t11 = time.time()
    stream.close()  #Streamをcloseする
    p_B.terminate()  #PyAudioインスタンスを終了する    
    str_data_B = b"".join(all)  #録音したデータのバイト型配列から文字列に変換
    #print(data)
    result = np.frombuffer(str_data_B,dtype="int16") / float(2**15)  #-1～1に正規化のためfloat(x)xの浮動小数点数への変換. #int16:符号付き16bit(=2byte)
    #np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-result"), result, fmt='%.5f')
    t12 = time.time()

def MakeAudioFile_B():
    global t13
    global t14
    global t15
    global t16
    global t17
    t13 = time.time()
    wavFile = wave.open(wavFileName_B, "wb")
    wavFile.setnchannels(CHANNELS_B)
    wavFile.setsampwidth(p_B.get_sample_size(FORMAT_B))
    wavFile.setframerate(RATE_B)
    wavFile.writeframes(str_data_B)
    wavFile.close()
    t14 = time.time()
    #MP3に圧縮
    mpeg = 'lame -V 2 '+FileName_B+'.wav ''/home/pi/Documents/admp441_data/'+FileName_B+'.mp3'
    subprocess.call(mpeg, shell=True)
    t15 = time.time()
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+FileName_B+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())
    t16 = time.time()
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    #ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq, np.abs(spec))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(freq, np.abs(spec))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("FFT", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(freq, np.abs(spec))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.show()
    plt.savefig('/home/pi/Documents/admp441_data/'+FileName_B+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+FileName_B+'.png', 'saved')
    t17 = time.time()
    
Recording_A()
#MakeAudioFile_A()
#time.sleep(1.0)
#Recording_B()
#MakeAudioFile_B()

index_loop = 1
while True:

    t40=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(Recording_B) #Recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(MakeAudioFile_A) #MakeAudioFile_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    t41 = time.time()
    result_A = executor.submit(Recording_A) #Recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(MakeAudioFile_B) #MakeAudioFile_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    t42 = time.time()
    index_loop += 1
    #print('基本情報の設定_A',t1-t0)
    print('Recording_A',t3-t0)
    print('MakeAudioFile_A',t8-t4)
    #print('基本情報の設定_B',t7-t6)
    print('Recording_B',t12-t9)
    print('MakeAudioFile_B',t17-t13)
    print('thread_1',t41-t40)
    print('thread_2',t42-t41)
    #memory
    memory = psutil.virtual_memory()
    print('memory.percent',memory.percent)
    #cpu
    cpu = psutil.cpu_percent(interval=1)
    print('cpu',cpu)
    #disk
    disk = psutil.disk_usage('/')
    print('disk.percent',disk.percent)


#g = np.frombuffer(g, dtype="int16") / float(2**15)
#frombuffer(x, dtype="int16")は、xを2バイト単位のデータが並んでいるバイナリデータとみなして、1次元配列にする。
#符号付2バイトなので、各要素の値は、-32768～32767 になります。

#x=frombuffer(x, dtype="int16")   #(1)
#x=x/32768                        #(2)
#と分けて書くことができます。(1)は上で説明した通りです。
#(2)は numpy では、「ndarray / 数値」で、「ndarray内の各要素を数値で割る」という処理を表現できます。
#このため -32768～32767 の値を 32768で割るため、各要素が -1以上1未満のfloat な ndarray になります。
#正規化
