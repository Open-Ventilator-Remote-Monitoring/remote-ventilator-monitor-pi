## Remote Ventilator Monitor - Raspberry Pi App

This git repo is for the code on the **Raspberry Pi**

### Architecture Overview
| [Heroku Cloud Server & Web Browser Repo](https://github.com/Open-Ventilator-Remote-Monitoring/ventilator-remote-monitoring) | Raspberry Pi (Network Adapter) Repo | [Ventilator (Arduino) Repo](https://github.com/Open-Ventilator-Remote-Monitoring/ventilator-monitor-arduino) |
| ----------- | ----------- | ----------- |
| Ruby on Rails | Flask | Arduino Board |
| Javascript | Python | C++ |

### Goal
Create a lightweight Raspberry Pi application to serve as a network adapter to relay data from Arduino-Based ventilators to a central monitoring dashboard (javascript web-browser application).

### Caution
This software is currently only a concept - it is neither approved nor intended to be used in any medical setting.

### Why Raspberry Pi?
Many of the rapidly manufacturable ventiltor designs utilize and arduino-based control system which does not have a network interface. The raspberry pi provides this network interface, serving as an API endpoint which can connect to central monitoring dashboard (javascript web-browser application). Raspberry pi's are cheap, easy to program, available in large quantities, locally sourceable, and reliable (by consumer hardwarwe standards).

### Current State of the App
**As of 11-April-2020:** Currently, the app is in demo/testing mode only.

### What Hardware do I need Development & Testing?
1. Obtain a Raspberry Pi board. Many raspberry pi's will work, but the [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) is widely available for an affordable price (~$ USD). These products are widely avialable, so shop around. [Newark](https://www.newark.com/buy-raspberry-pi) is the main US distributor and currently has about 56,000 [Raspberry Pi 4 Model B](https://www.newark.com/raspberry-pi/rpi4-modbp-4gb/raspberry-pi-4-model-b-4gb-rohs/dp/02AH3164)'s in stock for ~$55 USD each. 
2. Obtain a power supply and a The Rasperry Pi is power hungry, especially when you have an arduino plugged in, so be sure to pick up a beefy [power supply](https://www.newark.com/MarketingProductList?orderCode=03AH7034,07AH1285,07AH1286,07AH1287) if you don't already have one. Be sure to pick up the correct power supply for your board - the Raspberry Pi Model 4's now use a USB-C power supply instead of the old boards, which use a USB micro power supply. 
3. If you'll be using a display monitor with your pi (recommended - easier than headless mode) you will need the appropriate HDMI cable. Please note that the Raspberry Pi 4 now uses a mini-HDMI instead of a full size HDMI video cable.
4. Obtain an SD card - buy a high quality one with a good amount of memory. The Sandick Ultra Plus microSDHC UHS-I 32 GB seems to work nicely.
5. Obtain an SD card reader if you don't already have one.

### How do I set up my Raspberry Pi for Development & Testing?
Eventually we'll have pre-deployed images ready for download and quick install onto your SD card. For now, there is a lot of manual work:
1. Download the [SD Card Formatter](https://www.sdcard.org/downloads/formatter/index.html) tool to your desktop computer and format your SD card.
2. Download the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) for your desktop computer operating system.
3. Open the Raspberry Pi Imager and install the Rasbian Lite Image onto your SD card
4. Insert your SD card into your pi, connect your desktop monitor, keyboard, and mouse, and plug your pi into your power supply
5. When the pi boots, enter the default username: pi and password: raspberry
6. Either plug your raspberry pi into your local ethernet network or [add your wifi credentials to the wpa_supplicant.conf file](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).
7. The default hostname of the pi is `raspberrypi` which will make your pi accessible on your local network via the url http://www.raspberrypi.local. Here, we will change the host name to `ventilator-1` so the pi will be accessible on our LAN via the url http://www.ventilator-1.local. Change the host name of your raspberry pi using the nano ([new to nano?](https://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/)): `sudo nano /etc/hostname` -> change the host name to `ventilator-1` or similar. Use a different host name for each pi.
8. Edit the /etc/host file `sudo nano /etc/hosts` and change `raspberrypi` to `ventilator-1`
9. Update the apt package manager `sudo apt-get update`
10. Install git `sudo apt-get install git`
11. Install the python 3 package manager `sudo apt-get install python3-pip`
12. Install our application dependencies `sudo pip3 install flask flask-cors pyserial`
13. Clone this git repo: `git clone https://github.com/Open-Ventilator-Remote-Monitoring/remote-ventilator-monitor-pi.git`
14. `cd remote-ventilator-monitor-pi`
15. Intall the python dependencies for the virtual environment `pipenv install`
16. Open a virtual environment `sudo pipenv shell`
17. Update the `application-*.yml` files with the correct config
```yml
ventilator:
  name: <name of ventilator>
  connection:
    type: <random (testing) or serial(ardunio connection)>
    link: <serial port>
    baud: <baud speed>
    timeout: <timeout amount>
  alarm:
    pin: <-1 (testing) or gpio port on pi>
  device:
    id: <self set id of raspberry pi>
    roles:
      ventilatorAlarmSoundMonitor: <true(enable alarm plugin) or false(disable)>
      ventilatorDataMonitor: <true(enable ventilator plugin) or false(disable)>
```
18. Start the server using the start script: `FLASK_ENV=development FLASK_PORT=80 ./start.sh` (You may need to run `chmod 777 start.sh` first).
19. Open a web browser on your desktop (connected to the same network as your pi) and visit the url `http://ventilator-1.local` You should see the index info page. 
20. After you connect your properly programmed Arduino via a USB cable, you should be able to visit `http://ventilator-1.local/api/ventilator` and view JSON result of the latest ventilator stats. Refresh the page to query the Arduino again and get different values.

### Local Simulation

If you would like to run the web UI and hit a local simulation interface, make sure you have
all the dependencies installed:
1. `pivenv install`
2. Run the dev start script: `./start_dev.sh`
3. You should now be able to hit `localhost:5000/api/ventilator` and get the JSON response back.

You can also run it under the gunicorn script in dev mode:

`FLASK_ENV=development ./start.sh`

The `start.sh` script supports two environmental variables, FLASK_PORT and FLASK_LISTEN, if you need
to customize the port and listen address of the app, like this:

**Having a problem?** Leave a message on the Slack Channel or an issue on the Github and we'll help you out.
