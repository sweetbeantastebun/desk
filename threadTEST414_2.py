# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread  #スレッド処理するライブラリ
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed  #複数の処理を並列実行するためのライブラリ
import psutil  #Hardware情報（CPU,memory使用率）を確認するライブラリ

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)

def recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)
    #録音実行（16ビット量子化、44.1kHz）
    record = 'arecord -d 10 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()

def FFT_A():
    global t2
    global t3
    global t7
    global wavfile_A
    t2 = time.time()
    #wavファイルの読み込み
    wavfile_A = '/home/pi/Documents/admp441_data/'+filename_A+'.wav'
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #print('samples',len(samples))
    t3 = time.time()
    #t4 = time.time()
    #スペクトルをプロット表示
    spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2 + 1)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2 + 1)]    #周波数がマイナスになる周波数要素の削除
    #t5 = time.time()
    #グラフ作成
    plt.ion()
    plt.clf()
    #fig = plt.figure(figsize=(10,10),dpi=100)
    #ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(frequency_A, np.abs(spectrum_A))
    plt.axis([0,fs/2,0,100])
    plt.grid(which="both")
#    plt.xscale("log")
#    plt.yscale("log")
#    plt.axis([0,fs/2,0,10000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("Amplitude Spectrum", fontsize=12)
    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(frequency_A, np.abs(spectrum_A))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 100)
    #plt.grid(which="both")
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("Amplitude Spectrum", fontsize=12)

    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(frequency_A, np.abs(spectrum_A))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.savefig('/home/pi/Documents/admp441_data/Graph.png')
    plt.draw()
    plt.pause(1)
    #plt.close()
    #print('/home/pi/Documents/admp441_data/'+filename_A+'.png', 'saved')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f')
    
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t7 = time.time()

def recording_B():
    global t8
    global t9
    t8 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)        
    #録音実行（16ビット量子化、44.1kHz)
    record = 'arecord -d 10 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_B+'.wav'
    subprocess.call(record, shell=True)
    t9 = time.time()

def FFT_B():
    global t10
    global t11
    global t14
    global wavfile_B
    t10 = time.time()
    #wavファイルの読み込み
    wavfile_B = '/home/pi/Documents/admp441_data/'+filename_B+'.wav'
    wr = wave.open(wavfile_B, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #print('samples',len(samples))
    t11 = time.time()
    #t12 = time.time()
    #スペクトルをプロット表示
    spectrum_B = np.fft.fft(samples)  #2次元配列(実部，虚部)
    frequency_B = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    spectrum_B = spectrum_B[:int(spectrum_B.shape[0]/2 + 1)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_B = frequency_B[:int(frequency_B.shape[0]/2 + 1)]    #周波数がマイナスになる周波数要素の削除
    #t13 = time.time()
    #グラフ作成
    print('before')
    plt.ion()
    print('plt.作成')
    plt.clf()
    #plt.close()
    print('plt.clf後')
    #fig = plt.figure(figsize=(10,10),dpi=100)
    #ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(frequency_B, np.abs(spectrum_B))
    plt.axis([0,fs/2,0,100])
    plt.grid(which="both")
#    plt.xscale("log")
#    plt.yscale("log")
#    plt.axis([0,fs/2,0,10000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("Amplitude Spectrum", fontsize=12)
    #ax2 = fig.add_subplot(2, 2, 3)
    #plt.plot(frequency_B, np.abs(spectrum_B))
    #plt.xlim(0, 1000)
    #plt.ylim(0, 100)
    #plt.grid(which="both")
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.ylabel("Amplitude Spectrum", fontsize=12)
    print('グラフ作成後、出力前')
    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(frequency_B, np.abs(spectrum_B))
    #plt.xlim(0, 10000)
    #plt.ylim(0, 10000000)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    #plt.savefig('/home/pi/Documents/admp441_data/Graph.png')
    print('plgファイルをディレクトリに保存後')
    plt.draw()
    plt.pause(1)
    #plt.close()
    print('タスク終了')
    #print('/home/pi/Documents/admp441_data/'+filename_B+'.png', 'saved')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'spectrum', np.abs(spectrum_B), delimiter = " ", fmt='%.2f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'frequency', frequency_B, delimiter = " ", fmt='%.2f')
    
    #wavファイル削除
    file = filename_B + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t14 = time.time()

recording_A()
#FFT_A()
#recording_B()
#FFT_B()

#ここから無限ループ。
#並列処理でレコード中に音声解析(FFT)を実行する。
#タスクを4つ(recording_AとB、FFT_AとB)作成し、
#recording_BとFFT_Aの組み合わせ(recording_B実行中にFFT_Aを処理)
#recording_AとFFT_Bの組み合わせ(recording_A実行中にFFT_Bを処理)
#で処理していく。
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
#    index_loop += 1

#except KeyboardInterrupt:
#    print('!!FINISH!!')
