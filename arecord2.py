import subprocess
from datetime import datetime
import time
import csv

timestamp = datetime.today() #現在の日付、現在の時刻、ここでは測定開始時刻
print(timestamp)
record = "arecord -d 5 -f S16_LE -r 8000 test2.wav"

p = subprocess.Popen(record, shell=True)
t = 10  #sleepする時間（秒）を入力。録音時間の数字に合わせる。
time.sleep(t)

#レコード終了
print("Finished Recording.")
