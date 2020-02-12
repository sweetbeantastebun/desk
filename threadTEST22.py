# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from pydub import AudioSegment  #メディアデータの変換ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

t00 = time.time()

#ファイルの名前をタイムスタンプ化する
#def timestamp():
#    timestamp = datetime.today()
#    filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)

def recording_A():
    global t0
    global t2
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
            
    #録音実行（16ビット、44.1kHz、2秒）
    record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    #t1 = time.time()

    #MP3に圧縮             
    mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename_A+'.wav ''/home/pi/Documents/admp441_data/'+filename_A+'.mp3'
    subprocess.call(mpeg, shell=True)
    t2 = time.time()

def recording_B():
    global t3
    global t5
    t3 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
            
    #録音実行（16ビット、44.1kHz、2秒）
    record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_B+'.wav'
    subprocess.call(record, shell=True)
    #t4 = time.time()

    #MP3に圧縮             
    mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename_B+'.wav ''/home/pi/Documents/admp441_data/'+filename_B+'.mp3'
    subprocess.call(mpeg, shell=True)
    t5 = time.time()

def FFT_A():
    global t6
    global t7
    t6 = time.time()
    #timestamp = datetime.today()
    #filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename_A+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    t7 = time.time()

def graph_A():
    global t8
    global t9
    t8 = time.time()
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
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_A+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+filename_A+'.png', 'saved')
    t9 = time.time()

def FFT_B():
    global t10
    global t11
    t10 = time.time()
    #timestamp = datetime.today()
    #filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename_B+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    t11 = time.time()

def graph_B():
    global t12
    global t13
    t12 = time.time()
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
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_B+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+filename_B+'.png', 'saved')
    t13 = time.time()

recording_A()

index_loop = 1
while True:

    t14=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)
    result_B = executor.submit(recording_B) #recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(FFT_A) #FFT_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    t15 = time.time()
    result_A = executor.submit(recording_A) #recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(FFT_B) #FFT_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    t16 = time.time()
    index_loop += 1
    print('thread_1',t15-t14)
    print('thread_2',t16-t15)
    print('record_A',t2-t0)
    print('record_B',t5-t3)
    print('graph_A',t9-t8)
    print('graph_B',t13-t12)
    print('FFT_A',t7-t6)
    print('FFT_B',t11-t10)
#print(t8-t7)
#print(t9-t8)

#except KeyboardInterrupt:
#    print('!!FINISH!!')
