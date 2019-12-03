#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess


# In[2]:


from datetime import datetime


# In[3]:


import time


# In[4]:


import csv


# In[5]:


timestamp = datetime.today() #現在の日付、現在の時刻、ここでは測定開始時刻
print(timestamp)


# In[7]:


record = "arecord -d 5 -f S16_LE -r 8000 test2.wav"


# In[8]:


p = subprocess.Popen(record, shell=True)


# In[ ]:


t = 10  #sleepする時間（秒）を入力。録音時間の数字に合わせる。


# In[9]:


time.sleep(t)


# In[10]:


#レコード終了
print("Finished Recording.")

