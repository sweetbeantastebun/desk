# -*- coding: utf-8 -*-

import numpy as np  #配列計算、FFT化するライブラリ
import wave     #wavファイルの読み書きするライブラリ
import pyaudio  #録音機能を使うためのライブラリ
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ

timestamp = datetime.today()  #現在の日付、現在の時刻、ここでは測定開始時刻
print(timestamp)

wavFilename = datetime.today().strftime("%Y%m%d-%H%M%S") + ".wav"  #wavファイル名前を定義

def MakeWavFile(FileName = wavFilename, Record_Seconds = 2, save = True):
    #録音して（WAVファイル作成）、波形表示
    chunk = 1024  #音源から1回(1/RATE毎)読み込む時のデータサイズ。1024(=2**10)とすることが多い
    FORMAT = pyaudio.paInt16  #音源(=バイナリデータ)符号付き16ビット(-32768～32767)のバイナリ文字 #内訳,15ビット数字と1ビットの符号
    
    CHANNELS = 1  #モノラル。ステレオは2
    
    RATE = 44100  #サンプルレート,fs(個/sec),44.1kHz
                  #その逆数がサンプル周期 Ts(sec/個)
                  #fs=44.1kHz,1/fs=Ts=22.7μsec毎に1点データ取得  
    p = pyaudio.PyAudio()  #PyAudioインスタンスを作成する
    
    stream = p.open(format = FORMAT,  #入力用Streamを開く。
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)  #frames:pythonのwaveモジュールではバイナリデータ個数
    
    #レコード開始
    print("Now Recording...")
    all = []  #append前に空リスト作成
    for i in range(0, int(RATE / chunk * Record_Seconds)):  #整数化。RATEをChunkで割り切れる数に合わせる。
        data = stream.read(chunk)  #音声を読み取る。
        all.append(data)  #データを追加
    
    #レコード終了
    print("Finished Recording.")
    
    stream.close()  # Streamをcloseする
    p.terminate()  # PyAudioインスタンスを終了する    
    data = b"".join(all)  #録音したデータを配列に変換
    result = np.frombuffer(data,dtype="int16") / float(2**15)  #-1～1に正規化のため、float(x)xの浮動小数点数への変換
                                                               #int16:符号付き16bit(=2byte)
    #グラフ化        
    fig = plt.figure(figsize=(10,5))
    plt.plot(result)
    plt.xlabel("time [sample]", fontsize=12)
    plt.ylabel("amplitude", fontsize=12)
    plt.style.use("ggplot")
    plt.show()                 
    
    if(save): 
        wavFile = wave.open(FileName, "wb")
        wavFile.setnchannels(CHANNELS)
        wavFile.setsampwidth(p.get_sample_size(FORMAT))
        wavFile.setframerate(RATE)
        wavFile.writeframes(b"".join(all)) 
        wavFile.close()

if __name__ is "__main__":
    MakeWavFile()    

def ReadWavFile(FileName = wavFilename):
    #wavファイルを読み込み、高速フーリエ変換（FFT）
   
    try:
        wr = wave.open(FileName, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    except FileNotFoundError:  #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + FileName)
        return 0
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    g = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    g = np.frombuffer(g, dtype="int16") / float(2**15)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #時間信号をCSVファイルに出力
    #np.savetxt("sample1.csv", g, fmt='%.5f')
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-g"), g, fmt='%.5f')
             
    N = 65536  #サンプル数
    n0 = 0  #サンプリング開始位置
    F = np.fft.fft(g[n0:n0+N])  #高速フーリエ変換
    amp = [np.sqrt(c.real**2 +c.imag**2) for c in F]  #振幅スペクトル
    flist = np.fft.fftfreq(N,d=1.0/fs)  #周波数リスト   
    #周波数信号をテキストファイルに出力
    #np.savetxt("sample2.csv", flist, fmt='%.1f')
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-flist"), flist, fmt='%.1f')
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-amp"), amp, fmt='%.1f')
    
    #グラフ化する命令文
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(flist, amp)
    plt.axis([0,fs/2,0,100])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(flist, amp)
    plt.xlim(0, 3000)
    plt.ylim(0, 60)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax3 = fig.add_subplot(2, 2, 4)
    plt.plot(flist, amp)
    plt.xlim(4000, 18000)
    plt.ylim(0, 60)
    plt.xlabel("freqency(Hz)", fontsize=12)
    
    plt.tight_layout()  #グラフの位置やサイズが自動で調整されて、出力画像からのはみ出しを抑えることができるコード。
    plt.show()

if __name__ is "__main__":   
    ReadWavFile() 


    
    
    
#g = np.frombuffer(g, dtype="int16") / float(2**15)
#frombuffer(x, dtype="int16")は、xを2バイト単位のデータが並んでいるバイナリデータとみなして、1次元配列にする。
#符号付2バイトなので、各要素の値は、-32768～32767 になります。

#x=frombuffer(x, dtype="int16")   #(1)
#x=x/32768                        #(2)
#と分けて書くことができます。(1)は上で説明した通りです。
#(2)は numpy では、「ndarray / 数値」で、「ndarray内の各要素を数値で割る」という処理を表現できます。
#このため -32768～32767 の値を 32768で割るため、各要素が -1以上1未満のfloat な ndarray になります。
#正規化
