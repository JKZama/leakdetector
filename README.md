# Localized Leak Detector
This project is for the 4096/4097 CpE/EE courses at Missouri University of Science & Technology.
All libraries used are under an LGPL or less restrictive license.

Main node software is designed to be tested and run on a Raspberry Pi 3 Model B
Sensor node sofware is designed to be tested and run on an Arduino Uno R3
Sensors used on each node: DHT-22 and analog water level sensor

Software should work with any UART compatible physical layer.
We used MAX485 chips with receiver and driver pins connected to serial TX/RX on all sensor nodes.
DriverEnable/ ReceiverEnable-Complement pins were tied together and connected to D2 pin on sensor nodes.
A generic USB to RS-485 converter was used on the host node which is recognized as ch341-uart by the Pi.
