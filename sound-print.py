import serial # for serial port
import numpy as np # for arrays, numerical processing

#define the serial port.
port = "/dev/tty.uart-88FF466E374A1C39" #For Mac

with serial.Serial(port,9600,timeout = 0.050) as ser:
    print(ser.name)
    while(1): #loop forever
        data = ser.read(1)     # look for a character from serial port - will wait for up to 50ms (specified above in timeout)
        if len(data) > 0: #was there a byte to read?
            if ord(data)!=0:
                print(ord(data))
