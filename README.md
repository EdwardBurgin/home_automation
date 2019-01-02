# home_automation

Use 3.3v GPIO output from BCM 21 of rpi (top right header opposite 5v). Using a 4.7kv resistor, so not parasite mode. https://raspberrypi.stackexchange.com/questions/78134/how-to-use-ds18b20-in-parasite-power-mode/78175 {"""The DS18B20 needs at max 1.5mA for a conversion. Simultaneous conversions on several DS18B20 aren't allowed in parasite powered mode, so that's the maximum current you have to provide.

Use a 1kΩ pullup resistor to 3.3V, that provides up to 3.3mA and is sinkable by both the host and the DS18B20 without problems. You never run into the problem described in the datasheet.

The only reason you want to use the "strong pullup" (and the pullup option of the w1-gpio overlay) is minimizing power consumption, getting rid of these 3.3mA. If you wanted this, you had to connect the 1kΩ resistor to that specified pullup pin instead of +3.3V."""}

Set the one wire (w1) data line to be BCM 6 instead of default 4

check w1 dir at {cd /sys/bus/w1/devices} and find 28-xxxx device dir and cat w1-slave, read t=..... and divide 1000 for temp in degrees.

https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor

Changing the w1 dir so that a shield doesn't need to be modified:
https://pinout.xyz/pinout/1_wire
sudo dtoverlay w1-gpio gpiopin=4 pullup=0  # header pin 7


Original temp sensor datasheet: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware


More on Energenie pi-motes: 
https://energenie4u.co.uk/res/pdfs/ENER314%20UM.pdf
https://www.raspberrypi.org/blog/controlling-electrical-sockets-with-energenie-pi-mote/
https://github.com/Energenie/pyenergenie
https://github.com/whaleygeek/pyenergenie
https://opinionatedgeek.com/Snaplets/Blog/Form/Item/000751/Read


Pi pinout: https://www.google.com/search?q=raspberry+pi+2+pinout&safe=off&rlz=1C5CHFA_enIE732IE732&tbm=isch&source=iu&ictx=1&fir=oL4JD9fUyFm3PM%253A%252C1s2C61VHqmyqDM%252C_&usg=AI4_-kScykd95Dp9XLPMzpHLEyCahoflxA&sa=X&ved=2ahUKEwj1ocvWy8_fAhVL-6QKHe8QB8YQ9QEwAHoECAUQBA#imgrc=NtnLn40CvsfPgM:


