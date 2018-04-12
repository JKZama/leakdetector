
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
    defaultEmail = "localizedleakdetector@gmail.com"
    #logger = modbus_tk.utils.create_logger("console")
    while True:
        try:
            sleep(2)
            humidity = 1
            water = 1
            temp = 1
            data = ''
            nodeArray = [1]
            i = 0
            while i < len(nodeArray):
                if sys.argv[1:]:
                    email = sys.argv[1]
                else:
                    email = defaultEmail
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
                print("Node " + str(i))
                print("Water: " + str(water) + "\tHumidity: " + str(humidity))
                if(humidity>80 or water>100):
                    print("Leak detected at node " + str(i))
                    print("Alert sent via email to "+email)
                    print("Waiting for sensor readings to return to normal...")
                    mailsend.sendLeakAlertEmail(email,1)
                    while(humidity>70 or water>100):
                        data = master.execute(i, cst.READ_INPUT_REGISTERS, 0, 3)
                        humidity = data[1]
                        water = data[2]
                        sleep(2)
                        print("..")
                    print("Sensor readings returned to average")
                except modbus_tk.modbus.ModbusError as exc:
                    logger.error("%s- Code=%d", exc, exc.get_exception_code())
                    try:
                        data = master.execute(i,cst.READ_INPUT_REGISTERS, 0, 3)
                    except modbus_tk.modbus.ModbusError as exc:
                        logger.error("%s- Code=%d", exc, exc.get_exception_code())
if __name__ == "__main__":
    main()
