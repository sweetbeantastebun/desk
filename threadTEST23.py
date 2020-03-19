# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from pydub import AudioSegment  #メディアデータの変換ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed  #複数の処理を並列実行するためのライブラリ
import psutil  #Hardware情報（CPU,memory使用率）を確認するライブラリ

t00 = time.time()

def recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)
    #録音実行（16ビット、44.1kHz）
    record = 'arecord -d 5 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()

def FFT_A():
    global t2
    global t3
    global t7
    t2 = time.time()
    #MP3に圧縮
    mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename_A+'.wav ''/home/pi/Documents/admp441_data/'+filename_A+'.mp3'
    subprocess.call(mpeg, shell=True)
    t3 = time.time()
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename_A+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())  #音声データをリストで受け取る(配列データの取り出し)
    #t4 = time.time()
    #スペクトルをプロット表示
    spec_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    freq_A = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    spec_A = spec_A[:int(spec_A.shape[0]/2 + 1)]    #周波数がマイナスになるスペクトル要素の削除
    freq_A = freq_A[:int(freq_A.shape[0]/2 + 1)]    #周波数がマイナスになる周波数要素の削除
    #t5 = time.time()
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq_A, np.abs(spec_A))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(freq_A, np.abs(spec_A))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("FFT", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(freq_A, np.abs(spec_A))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_A+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+filename_A+'.png', 'saved')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'spec', np.abs(spec_A), delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'freq', freq_A, delimiter = " ", fmt='%.2f')
    t7 = time.time()

def recording_B():
    global t8
    global t9
    t8 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)        
    #録音実行（16ビット、44.1kHz)
    record = 'arecord -d 5 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_B+'.wav'
    subprocess.call(record, shell=True)
    t9 = time.time()

def FFT_B():
    global t10
    global t11
    global t14
    t10 = time.time()
    #MP3に圧縮
    mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename_B+'.wav ''/home/pi/Documents/admp441_data/'+filename_B+'.mp3'
    subprocess.call(mpeg, shell=True)
    t11 = time.time()
    #mp3の読み込み
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename_B+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())  #音声データをリストで受け取る(配列データの取り出し)
    #t12 = time.time()
    #スペクトルをプロット表示
    spec_B = np.fft.fft(samples)  #2次元配列(実部，虚部)
    freq_B = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    spec_B = spec_B[:int(spec_B.shape[0]/2 + 1)]    #周波数がマイナスになるスペクトル要素の削除
    freq_B = freq_B[:int(freq_B.shape[0]/2 + 1)]    #周波数がマイナスになる周波数要素の削除
    #t13 = time.time()
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq_B, np.abs(spec_B))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(freq_B, np.abs(spec_B))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("FFT", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(freq_B, np.abs(spec_B))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_B+'.png')
    plt.close()
    #print('/home/pi/Documents/admp441_data/'+filename_B+'.png', 'saved')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'spec', np.abs(spec_B), delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'freq', freq_B, delimiter = " ", fmt='%.2f')
    t14 = time.time()

recording_A()
#FFT_A()
#recording_B()
#FFT_B()

#index_loop = 1
while True:

    t16=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(recording_B) #recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(FFT_A) #FFT_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    t17 = time.time()
    result_A = executor.submit(recording_A) #recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(FFT_B) #FFT_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    t18 = time.time()
    #index_loop += 1
    print('thread_1',t17-t16)
    print('thread_2',t18-t17)
    print('record_A',t1-t0)
    print('record_B',t9-t8)
    print('FFT_A',t7-t2)
    print('FFT_B',t14-t10)
    #memory使用率を出力
    memory = psutil.virtual_memory()
    print('memory.percent',memory.percent)
    #cpu使用率を出力
    cpu = psutil.cpu_percent(interval=1)
    print('cpu',cpu)
    #diskの容量を出力
    disk = psutil.disk_usage('/')
    print('disk.percent',disk.percent)

#except KeyboardInterrupt:
#    print('!!FINISH!!')
