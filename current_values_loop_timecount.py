#!/usr/bin/env

import time
import sys
import numpy as np
import csv
#import pandas as pd

t00=time.time()
#print(sys.path)

sys.path.append('/home/pi/Documents/adxl355')

#print(sys.path)

#time.sleep(1)

from adxl355 import ADXL355

device = ADXL355()


loop_num = 4096
loop_int = 0.0001 #可変

'''
x = []
y = []
z = []
'''

#time.sleep(0.1)
print('start')

index=1
while index <= 50:
    
    t1=time.time()
    
    xyz = []


    index2=0
    while index2 < loop_num:
        axes = device.get_axes() # pylint: disable=invalid-name
        xyz.append(axes)
        time.sleep(loop_int)
        index2 += 1

    t2=time.time()


    print('data get 4000', t2-t1)

    data = np.array(xyz)
    #print(data)

    #csv書き込み時間計測
    t3=time.time()

    header = ['xg','yg','zg']

    with open('/home/pi/Documents/adxl355/adxl355_data/adxl355csv'+str(index)+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    #t4=time.time()

    index += 1

    t4=time.time()
    print('write csv', t4-t3)
    print('get data and write csv', t4-t1)

    
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    #print(x)
    #print(y)
    #print(len(z))
    x_dup = []
    y_dup = []
    z_dup = []
    #データ重複確認
    for i in range(loop_num):
        if x[i-1]==x[i]:
           #print("x data dupulicated!")
           #print(i)
           x_dup.append(i)

    for i in range(loop_num):
        if y[i-1]==y[i]:
            #print("y data dupulicated!")
            #print(i)
            y_dup.append(i)
    for i in range(loop_num):
        if z[i-1]==z[i]:
            #print("z data dupulicated!")
            #print(i)
            z_dup.append(i)

    print("x_len", len(x_dup))
    print("y_len", len(y_dup))
    print("z_len", len(z_dup))
    
