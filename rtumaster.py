
#!/usr/bin/env python
# -*- coding: utf_8 -*-

# Modbus TestKit: Implementation of Modbus protocol in python
# (C)2009 - Luc Jean - luc.jean@gmail.com
# (C)2009 - Apidev - http://www.apidev.fr
# This is distributed under GNU LGPL license, see license.txt

# This library has been modified for the leak detect project
# by Jesse Zamazanuk
from time import sleep
import mailsend
import sys
import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

#PORT = 1
PORT = '/dev/ttyUSB0'

def main():
    #logger = modbus_tk.utils.create_logger("console")
    while True:
        try:
            humidity = 1
            water = 1
            temp = 1
            data = ''
            if sys.argv[1:]:
                email = sys.argv[1:]
            #Connect to the slave
            master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
            master.set_timeout(5.0)
            master.set_verbose(False)
            #logger.info("connected")
            #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 0, 3))
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 3)
            water = data[0]
            humidity = data[1]
            temp = data[2]
            print("Water: " + str(water) + "\tHumidity: " + str(humidity))
            if(humidity>80 or water>100):
                print("Leak Detected!")
                print("Alert sent via email")
                print("Waiting for sensor readings to return to normal...")
                mailsend.sendLeakAlertEmail("jkzq62@mst.edu", 1)
                while(humidity>70 or water>100):
                    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 3)
                    humidity = data[1]
                    water = data[2]
                    sleep(2)
                    print("..")
                print("Sensor readings returned to average")
        except modbus_tk.modbus.ModbusError as exc:
            logger.error("%s- Code=%d", exc, exc.get_exception_code())
            try:
                data = master.execute(1,cst.READ_INPUT_REGISTERS, 0, 3)
            except modbus_tk.modbus.ModbusError as exc:
                logger.error("%s- Code=%d", exc, exc.get_exception_code())
        sleep(2)
if __name__ == "__main__":
    main()
