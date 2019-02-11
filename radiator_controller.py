import matplotlib
matplotlib.use('Agg')
import collections
import datetime
import numpy as np
import pickle
import matplotlib.pyplot as plt
from util import *

temps = collections.deque(maxlen=24*60)
message_log = collections.deque(maxlen=24*60)
time.sleep(0.2)
wireless_ini()
time.sleep(0.2)
print('SENDING OFF SIGNAL')
wireless_one_off()

print('entering loop')
while True:
    file_log = open('log.txt','w')
    t = datetime.datetime.now().time()
    curr = read_temp()
    temps.append((t, curr))

    if (curr <= 15) & (t.hour < 8):
        message = '%d:%d Temp: %.3f, turning on the radiator'%(t.hour, t.minute, curr)
        print(message)
        message_log.appendleft(message)
        #wireless_ini()
        wireless_one()
    elif (curr > 15.5) or (t.hour > 8):
        message = '%d:%d Temp: %.3f, turning OFF radiator'%(t.hour, t.minute,curr)
        print(message)
        message_log.appendleft(message)
        #wireless_ini()
        wireless_one_off()
    else:
        message = '%d:%d Temp:%.3f '%(t.hour, t.minute, curr)
        message_log.appendleft(message)
    
    file_log = open('log.txt','w')
    file_log.write("\n <br />".join(message_log))
    file_log.close()
    plt.plot([i[1] for i in temps])
    plt.savefig('graph.png')
    plt.close()
    time.sleep(600)

