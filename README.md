# Remote Ventilator Monitor - Raspberry Pi App
### Goal
Create a lightweight Raspberry Pi application to serve as a network adapter to relay data from Arduino-Based ventilators to a central monitoring dashboard (javascript web-browser application).

### Caution
This software is currently only a concept - it is neither approved nor intended to be used in any medical setting.

### Why Raspberry Pi?
Many of the rapidly manufacturable ventiltor designs utilize and arduino-based control system which does not have a network interface. The raspberry pi provides this network interface, serving as an API endpoint which can connect to central monitoring dashboard (javascript web-browser application). Raspberry pi's are cheap, easy to program, available in large quantities, locally sourceable, and reliable (by consumer hardwarwe standards).

### Current State of the App
**As of 3-April-2020:** Currently, the app is in demo/testing mode only. The server consists of a python flask app. A typical data request from the dashboard is handled like this: 
1. The flask app receives a request from the javascript dashboard application
2. The flask app sends a request to the ventilator (Arduino) for data via the USB serial cable
3. The flask app receives the data back from the ventilator (Arduino)
4. The flask app sends the data to the javascript dashboard application

### How do I set up a Raspberry Pi for Development & Testing?
1. Obtain a raspberry pi. Many raspberry pi's will work, but the [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) is widely available for an affordable price (~$ USD). These products are widely avialable, so shop around. [Newark](https://www.newark.com/buy-raspberry-pi) is the main US distributor and currently has about 56,000 [Raspberry Pi 4 Model B](https://www.newark.com/raspberry-pi/rpi4-modbp-4gb/raspberry-pi-4-model-b-4gb-rohs/dp/02AH3164)'s in stock for ~$55 USD each. The Rasperry Pi is power hungry, especially when you have an arduino plugged in, so be sure to pick up a beefy [power supply](https://www.newark.com/MarketingProductList?orderCode=03AH7034,07AH1285,07AH1286,07AH1287) if you don't already have one. Be sure to pick up the correct power supply for your board - the Raspberry Pi Model 4's now use a USB-C power supply instead of the old boards, which use a USB micro power supply. Also note that the new Raspberry Pi 4 uses a mini-HDMI instead of a full size HDMI video cable.
