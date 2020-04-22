import matplotlib.pyplot as plt
import random
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed


def random_A():
    print('random_A running')
    index = 1
    while index <= 5:
        global xa
        global ya
        xa = []
        ya = []
        for i in range(10):
            a = random.random()
            b = random.random()
            xa.append(a)
            ya.append(b)
        print(xa)
        print(ya)
        index += 1
    time.sleep(2)
    print('random_A finished')

def random_B():
    print('random_B running')
    index = 1
    while index <= 5:
        global xb
        global yb
        xb = []
        yb = []
        for i in range(10):
            a = random.random() + 10
            b = random.random() + 10
            xb.append(a)
            yb.append(b)
        print(xb)
        print(yb)
        index += 1
    time.sleep(2)
    print('random_B finished')

def graph_A():
    print('graph_A running')
    plt.ion()  # ←追加　　　　インタラクティブモードON
    plt.clf()  # ←追加  　他にplt.cla()、plt.close()
    plt.title('graph_A')
    plt.plot(xa, ya)
    plt.draw()  # ←showからdrawに変更
    plt.pause(1)  # ←追加　　　　表示させたい時間
    print('graph_A finished')

def graph_B():
    print('graph_B running')
    plt.ion()  # ←追加　　　　インタラクティブモードON
    plt.clf()  # ←追加  　他にplt.cla()、plt.close()
    plt.title('graph_B')
    plt.plot(xb, yb)
    plt.draw()  # ←showからdrawに変更
    plt.pause(1)  # ←追加　　　　表示させたい時間
    print('graph_B finished')

random_A()
index = 0
while index <= 100:
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(random_B())
    executor.submit(graph_A())
    as_completed([result_B]).__next__()
    result_A = executor.submit(random_A())
    executor.submit(graph_B())
    as_completed([result_A]).__next__()
    index += 1
