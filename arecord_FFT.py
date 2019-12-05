import subprocess
from datetime import datetime
timestamp = datetime.today()
print(timestamp)
record = "arecord -d 5 -f S32_LE -r 44100 test.wav"
subprocess.call(record, shell=True)

import numpy as np  #配列計算、FFT化するライブラリ
import wave     #wavファイルの読み書きするライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ

timestamp = datetime.today() #現在の日付、現在の時刻、ここでは測定開始時刻
print(timestamp)

def ReadWavFile(FileName = "test.wav"):
    #wavファイルを読み込み、高速フーリエ変換（FFT）
    try:
        wr = wave.open(FileName, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + FileName)
        return 0
    
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理） 
    g = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    g = np.frombuffer(g, dtype="int32") / float(2**31)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #時間信号をCSVファイルに出力
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-g"), g, fmt='%.5f')
                
    N = 32768  #サンプル数
    n0 = 0  #サンプリング開始位置
    F = np.fft.fft(g[n0:n0+N])  #高速フーリエ変換          
    amp = [np.sqrt(c.real**2 +c.imag**2) for c in F]  #振幅スペクトル
    flist = np.fft.fftfreq(N,d=1.0/fs)  #周波数リスト
    #周波数信号をCSVファイルに出力（整数表示）
    #np.savetxt("sample2.csv", flist, fmt='%.1f')
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-flist"), flist, fmt='%.1f')
    np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-amp"), amp, fmt='%.1f')
    
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(flist, amp)
    plt.axis([0,fs/2,0,100])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(flist, amp)
    plt.xlim(0, 500)
    plt.ylim(0, 100)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax3 = fig.add_subplot(2, 2, 4)
    plt.plot(flist, amp)
    plt.xlim(500, 4000)
    plt.ylim(0, 100)
    plt.xlabel("freqency(Hz)", fontsize=12)
    
    plt.tight_layout()
    plt.show()

if __name__ is "__main__":
    ReadWavFile()       
