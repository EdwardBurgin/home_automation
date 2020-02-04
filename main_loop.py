from IPython.display import HTML
# from ipywidgets import widgets
# from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display, Image

import gc

import pandas as pd
import collections
import datetime
import numpy as np
# import pickle
# import util
# from multiprocessing import Process
import sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from util import *

proc = None
temps = collections.deque(maxlen=144)
message_log = collections.deque(maxlen=200)

temp_ini()
wireless_ini()

def plot_fn(d):
    '''
    Place plotting in limited scope.
    '''
    import matplotlib
    matplotlib.use('Agg')
#     import seaborn as sns
#     import matplotlib.pyplot as plt
    from matplotlib.pyplot import savefig, plot, close, clf, cla, subplots, xticks
    
#         fig=plt.figure()
#         ax = fig.add
#         
#         plt.figure()
#         plt.plot()
    fig, ax= subplots(figsize=(12,3))
    ax.plot(d)
#         sns.lineplot(data = d, style = 'event', ci = 'sd', err_style='band', ax=ax)
    _ = xticks(rotation = 30)
    savefig('graph.png')
    close('all')
#         plt.show()a
#         plt.show(block=False)
#     plt.close(fig)
#     plt.close('all')
#     plt.close()
#     plt.clf()
#     plt.cla()
    del ax
    del fig
    del d
    gc.collect()
    
    
def radiator_controller(temp_lower, time_finish, interval_load):
    """
    Reads temperature, appends to limited width buffer which is writen to a txt file.
    Also plots a graph should another process wish to view the graph
    There is a delta of the temperature_min, where it does nothing.
    """
    while True:
        file_log = open('log.txt','w')
        t = datetime.datetime.now()
        tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])  #linux only
        curr = read_temp()
        temps.append((t, curr))
        if (curr <= temp_lower) & (t.hour < time_finish):
            message = 'date:%d %d:%d:%d Temp: %.3f, turning on the radiator. PARAM:ideal_temp %s end_time %d int%d'%(t.day, t.hour, t.minute,t.second, curr, temp_lower, time_finish, interval_load)
            message_log.appendleft(message)
            wireless_one()
#             print('trigger ', curr, time_finish, t.hour)
            sys.stdout.write("%s  \r" % (message) )
            sys.stdout.flush()

        elif (curr > (temp_lower + 0.2)) or (t.hour >= time_finish):
            message = 'date:%d %d:%d:%d Temp: %.3f, turning OFF radiator. PARAM:ideal_temp %s end_time %d int%d free_mem%d'%(t.day, t.hour, t.minute,t.second, curr, temp_lower, time_finish, interval_load,free_m)
            message_log.appendleft(message)
            wireless_one_off()
#             print('OFF ', curr, time_finish, t.hour)
            sys.stdout.write("%s  \r" % (message) )
            sys.stdout.flush()

        else:
            message = 'date:%d %d:%d:%d Temp:%.3f . PARAM:ideal_temp %s end_time %d int%d'%(t.day, t.hour, t.minute,t.second, curr, temp_lower, time_finish, interval_load)
            message_log.appendleft(message)
            sys.stdout.write("%s  \r" % (message) )
            sys.stdout.flush()

        file_log = open('log.txt','w')
        file_log.write("\n <br />".join(message_log))
        file_log.close()
#         plt.plot([i[1] for i in temps])
        d = pd.Series(index = [i[0] for i in temps], data = [i[1] for i in temps])#.plot(figsize=(20,7))
        plot_fn(d)
        
        if t.hour > time_finish:
            time.sleep(interval_load*4)
        else:
            time.sleep(interval_load)
#         %reset

print('hi, starting loop')        
radiator_controller(temp_lower=16.5, time_finish=8, interval_load=180)
