
# Home Automation

I have had a bunch of RPi units sitting around doing nothing, dumb RF smart plugs using a frequently lost clicker and a new echo devices. A first port of call was thermal regulation for my inadequately insulated rented accomodation. Then I want everything connected to and controlled by the Alexa.
Documenting to help others and remind/organise for myself for later.

## Results

Both heating activation time range and temperature zoning work as expected as seen in the image below:

![Graph1](https://github.com/EdwardBurgin/EdwardBurgin.github.io/blob/master/images/assorted/Screen%20Shot%202019-01-06%20at%2013.10.14.png )


### One Wire Temperature sensor

Use 3.3v GPIO output from BCM 21 of rpi (top right header opposite 5v). Using a 4.7kv resistor, so not parasite mode. https://raspberrypi.stackexchange.com/questions/78134/how-to-use-ds18b20-in-parasite-power-mode/78175 
```The DS18B20 needs at max 1.5mA for a conversion. Simultaneous conversions on several DS18B20 aren't allowed in parasite powered mode, so that's the maximum current you have to provide.

Use a 1kΩ pullup resistor to 3.3V, that provides up to 3.3mA and is sinkable by both the host and the DS18B20 without problems. You never run into the problem described in the datasheet.

The only reason you want to use the "strong pullup" (and the pullup option of the w1-gpio overlay) is minimizing power consumption, getting rid of these 3.3mA. If you wanted this, you had to connect the 1kΩ resistor to that specified pullup pin instead of +3.3V."""}
```
Set the one wire (w1) data line to be BCM 6 instead of default 4

check w1 dir at {cd /sys/bus/w1/devices} and find 28-xxxx device dir and cat w1-slave, read t=..... and divide 1000 for temp in degrees.

https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor

Changing the w1 dir so that a shield doesn't need to be modified:
https://pinout.xyz/pinout/1_wire


Add to the start of the raspberry pi initiation sequence:
`<sudo dtoverlay w1-gpio gpiopin=6 pullup=0  # header pin 7>`


Original temp sensor datasheet: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware


## Energenie pi-mote shield: 

- https://energenie4u.co.uk/res/pdfs/ENER314%20UM.pdf
- https://www.raspberrypi.org/blog/controlling-electrical-sockets-with-energenie-pi-mote/
- https://github.com/Energenie/pyenergenie
- https://github.com/whaleygeek/pyenergenie
- https://opinionatedgeek.com/Snaplets/Blog/Form/Item/000751/Read

## Pi pinout:

![pinout2](https://github.com/EdwardBurgin/EdwardBurgin.github.io/blob/master/images/assorted/gpio_layout-raspberry-pi2.jpg)

# Developing on the Raspberry pi

I love jupyter notebook, especially for rapid prototyping (hardware or software). To get this going follow this [blog](https://www.instructables.com/id/Jupyter-Notebook-on-Raspberry-Pi/) to setup jupyter. There is also something called Berryconda (this didn't work for me out of the box so saved for a later date).

```bash
sudo su -
apt-get update
apt-get install python3-matplotlib
apt-get install python3-scipy
pip3 install --upgrade pip
reboot
sudo pip3 install jupyter
```

Then on the pi start a server like this:
- On pi: nohup jupyter notebook --no-browser --port=8889
- Use htop to ensure running. don't close terminal as will kill kernal. (Recommend to use Tmux to give many panels in terminal)
- On LOCAL: ssh -N -f -L localhost:8890:localhost:8889 pi@192.168.1.xxx

## Python package management
Couple of options here (conda in the second link may be best): 
- https://github.com/googlesamples/assistant-sdk-python/issues/236
- https://gist.github.com/RobbieClarken/416d67ff6a0ffd631acd


