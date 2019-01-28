import matplotlib
matplotlib.use('Agg')
import collections
import datetime
import numpy as np
import pickle
import matplotlib.pyplot as plt
from util import *

temps = collections.deque(maxlen=24*60)
trigger_block = False
block_time = datetime.datetime.now().time()  # ini
t = datetime.datetime.now().time()
print('entering loop, turn off for clean start')
wireless_ini()
wireless_one_off()
while True:
    t = datetime.datetime.now().time()
    curr = read_temp()
    temps.append((t, curr))

    if (curr <= 17.0) & (t.hour < 9) & (trigger_block == False):
        print('Temp: %s at time: %s, turning on the radiator'%(curr, t))
        trigger_block = True
        wireless_ini()
        wireless_one()
    elif (curr > 17.5) & (trigger_block == True):
        wireless_ini()
        wireless_one_off()
        trigger_block = False
    plt.plot([i[1] for i in temps])
    plt.savefig('graph.png')
    time.sleep(60)
