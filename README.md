
# Home Automation

I have had a bunch of RPi units sitting around doing nothing, dumb RF smart plugs using a frequently lost clicker and a new echo devices. A first port of call was thermal regulation for my inadequately insulated rented accomodation. Then I want everything connected to and controlled by the Alexa. Currently controlled though a notebook with widgets, exposed to the local network so controlled through any internet accessible device.
Documenting to help others and remind/organise for myself for later.

![Setup](https://github.com/EdwardBurgin/EdwardBurgin.github.io/blob/master/images/assorted/20190106_131101.jpg )

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
This can be added to /boot/config.txt


Original temp sensor datasheet: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware


## Energenie pi-mote shield: 

- https://energenie4u.co.uk/res/pdfs/ENER314%20UM.pdf
- https://www.raspberrypi.org/blog/controlling-electrical-sockets-with-energenie-pi-mote/
- https://github.com/Energenie/pyenergenie
- https://github.com/whaleygeek/pyenergenie
- https://opinionatedgeek.com/Snaplets/Blog/Form/Item/000751/Read

## Pi pinout:

![pinout2](https://github.com/EdwardBurgin/EdwardBurgin.github.io/blob/master/images/assorted/gpio_layout-raspberry-pi2.jpg)

# Pi setup
Use TMUX, remember to setup TPM and ressurect with continuum. Always forget the tpm bit so here's the link: https://github.com/tmux-plugins/tpm

# Enable SSH
sudo raspi-config

# Pi info
```
cat /proc/cpuinfo
cat /etc/debian_version
cat /etc/os-release
```

9.11  PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"
Pi 2 Model B	1GB	a01041 (Sony, UK)
a21041 (Embest, China)

## Docker and source on Pi for redis
Based on: 
- https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/
- https://thisdavej.com/guides/redis-node/installation.html
- https://habilisbest.com/install-redis-on-your-raspberrypi
 -Lots of ARM v7 containers here: https://hub.docker.com/u/arm32v7/
- Docker jupyter notebook: https://github.com/movalex/rpi-jupyter-conda
```
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker
docker --version
sudo nano /etc/sysctl.conf
vm.overcommit_memory = 1
```
# Developing on the Raspberry pi

I love jupyter notebook, especially for rapid prototyping (hardware or software). To get this going follow this [blog](https://www.instructables.com/id/Jupyter-Notebook-on-Raspberry-Pi/) to setup jupyter. There is also something called Berryconda (this didn't work for me out of the box so saved for a later date).

```
bash
sudo su -
apt-get update
apt-get install python3-matplotlib
apt-get install python3-scipy
pip3 install --upgrade pip
reboot
sudo pip3 install jupyter
sudo apt-get install python-pandas  #FIXED 2020 issue https://raspberrypi.stackexchange.com/questions/17073/how-do-i-install-pandas-on-raspberry-pi
```

Trouble after doing pip install pip --upgrade #don't do this
installed ARMv7 miniconda latest

Don't use miniconda, look for Berryconda instead, the following is for reference.
https://github.com/jjhelmus/berryconda

```
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
sudo md5sum Miniconda3-latest-Linux-armv7l.sh # (optional) check md5
sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh # -> change default directory to /home/pi/miniconda3
sudo nano /home/pi/.bashrc # -> add: export PATH="/home/pi/miniconda3/bin:$PATH"
sudo reboot -h now
sudo chown -R pi miniconda3
conda config --add channels rpi
conda update conda
conda install -c anaconda pandas
```

## To give the Pi a fixed IP on WLan:
sudo nano /etc/dhcpcd.conf
```
interface wlan0
static ip_address=192.168.0.200/24  #/24 is shortcut for 255.255.255.0
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

##  Then on the pi start a server like this:

- On pi: nohup jupyter notebook --no-browser --port=8889 --allow-root #nohup optional #root allows saving files on pi
- Use htop to ensure running. don't close terminal as will kill kernal. (Recommend to use Tmux to give many panels in terminal)
- On LOCAL: ssh -N -f -L localhost:8890:localhost:8889 pi@192.168.1.xxx
- WinSubLinux requires ssh -N -f -L 127.0.0.1:8890:localhost:8889 pi@192.168.1.13

nb. if the connection is broken and local says port is in use on reconnect use `lsof -i :8890 # can pipe this to kill command with | xargs kill -9`
nbb At somepoint set notebook to be accessible through local subnet, now requires --ip 0.0.0.0 to run jupyter without throwing error99.
(lsof on pi is not installed by default-use `sudo apt install lsof`)
## Python package management
Couple of options here (conda in the second link may be best): 
- https://github.com/googlesamples/assistant-sdk-python/issues/236
- https://gist.github.com/RobbieClarken/416d67ff6a0ffd631acd
`source ./etc/bin/activate`

python -m pip install --user seaborn

## TFT screen for Pi:
https://github.com/EdwardBurgin/Raspberry-Pi-Installer-Scripts/blob/master/adafruit-pitft.sh

## Mounting an SSD
https://www.raspberrypi.org/documentation/configuration/external-storage.md
https://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/ #better

```
ls -l /dev/disk/by-uuid/
sudo nano /etc/fstab```
```

```
##'UUID=5C50-E449 /mnt/ed_ssd vfat defaults,user,auto,rw,nofail 0 1'## permissions problem
UUID=5C50-E449 /media/plexmedia/ vfat auto,users,umask=000 0 0 #permission fixed
UUID=5C50-E449 /media/plexmedia vfat auto,nofail,noatime,users,rw,uid=pi,gid=pi 0 0#better with nofail noatime
```

``` 
sudo mkdir /media/plexmedia
sudo chown -R pi:pi /media/plexmedia
sudo reboot
```

## Pi network share with windows via samba
https://pimylifeup.com/raspberry-pi-samba/
sudo apt-get install samba samba-common-bin
sudo nano /etc/samba/smb.conf
```
[foldername1]
valid users=username1
public = no
writable = yes
browseable =yes
printable = no
create mask = 0755

[foldername2]
valid users=username1
public = no
writable = yes
browseable =yes
printable = no
create mask = 0755
```
Then..
sudo smbpasswd -a pi
sudo systemctl restart smbd

## Plex on Pi
https://pimylifeup.com/raspberry-pi-plex-server/
sudo apt-get install apt-transport-https #apt via https
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
sudo apt-get update #new repo so update
sudo apt-get install plexmediaserver

## FTP server on Pi
https://www.raspberrypi-spy.co.uk/2018/05/creating-ftp-server-with-raspberry-pi/

