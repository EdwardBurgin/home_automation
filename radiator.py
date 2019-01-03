
# coding: utf-8

# In[39]:


f= open("temp.txt","w+")
f.close()


# In[41]:


f= open("temp.txt","a+")
val = 3
f.write('%d\n'%val)
f.close()


# In[42]:


# f = open("temp.txt","r")
# for i in f:
#     print(i)


# In[ ]:


#import the required modules
import RPi.GPIO as GPIO

import time
# set the pins numbering mode
GPIO.setmode(GPIO.BOARD)
# Select the GPIO pins used for the encoder K0-K3 data inputs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
# Select the signal used to select ASK/FSK
GPIO.setup(18, GPIO.OUT)
# Select the signal used to enable/disable the modulator
GPIO.setup(22, GPIO.OUT)
# Disable the modulator by setting CE pin lo
GPIO.output (22, False)
# Set the modulator to ASK for On Off Keying
# by setting MODSEL pin lo
GPIO.output (18, False)
# Initialise K0-K3 inputs of the encoder to 0000
GPIO.output (11, False)
GPIO.output (15, False)
GPIO.output (16, False)
GPIO.output (13, False)


# ## temp

# In[ ]:


import os 
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21,1)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_loc = '/sys/bus/w1/devices/28-0213924576ef/'
os.chdir(temp_loc)
print(os.getcwd())
temp_sensor = 'w1_slave'

def temp_raw():
	f=open(temp_sensor,'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines=temp_raw()
	while lines[0].strip()[-3:]!='YES':
		time.sleep(0.2)
		lines = temp_raw()
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string)/1000.0
		return temp_c

while True:
	curr = read_temp()
    f= open("temp.txt","a+")
    f.write('%d\n'%curr)
    f.close()
    if curr < 17:
        print 'turning on radiator'
        GPIO.output (11, True)
		GPIO.output (15, True)
		GPIO.output (16, True)
		GPIO.output (13, True)
		# let it settle, encoder requires this
		time.sleep(0.1)
		# Enable the modulator
		GPIO.output (22, True)
		# keep enabled for a period
		time.sleep(0.25)
		# Disable the modulator
		GPIO.output (22, False)
	time.sleep(20)

