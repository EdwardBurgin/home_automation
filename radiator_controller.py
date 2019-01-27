import collections
import datetime
import numpy as np
import pickle

from util import *

temps = collections.deque(maxlen=24*60)
trigger_block = False
block_time = datetime.datetime.now().time()  # ini
t = datetime.datetime.now().time()
print('entering loop')
while True:
    t = datetime.datetime.now().time()
    curr = read_temp()
    # print(t, curr)
    temps.append((t, curr))

    if (curr <= 17.0) & (t.hour < 9) & (trigger_block == False):
        trigger_block = True
        wireless_ini()
        wireless_one()
    elif (curr > 17.5) & (trigger_block == True):
        wireless_ini()
        wireless_one_off()
        trigger_block = False

    time.sleep(60)