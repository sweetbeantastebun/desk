#coding:utf-8
"""
ディレクトリ内の複数wavファイルを一括で処理
FFT図の類似度を算出
"""
import time  #タイムカウントに使用するライブラリ
import numpy as np #行列、配列計算、FFT化するライブラリ
from scipy import signal  #信号処理や統計を使用するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import cv2  #画像処理ライブラリ

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


def Matching():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    csvFileName_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second)
    t1 = time.time()
    global t2
    global t3
    t2 = time.time()
    #画像の読み込み
    #デフォルト画像の読み込み
    img_DFT = cv2.imread(path + ".png")  #""の中にファイル名を入力
    #テンプレート画像の読み込み
    Template_File = glob.glob(path + "*.png")
    for TEMP_File in Template_File:
        img_TEMP = cv2.imread(TEMP_File)
        
        #テンプレートマッチングNCC（Normalized Cross Correlation正規化相互相関係数）
        method =cv2.TM_CCOEFF_NORMED
        #テンプレートマッチング算出
        result = cv2.matchTemplate(img_TEMP, img_DFT, cv2.TM_CCOEFF_NORMED)
        #最小値、最大値、座標を取得
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        #ファイル名、類似度を格納
        RESULT = [TEMP_File,round(max_value,4)]
        
        #csv
        with open(path +csvFileName_A+ ".csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([RESULT])
        t3 = time.time()
Matching()
print("finish")
#except KeyboardInterrupt:
#print("FINISH!")
