"""

#Author: Sean Sill
#email: sms3h2@gmail.com
#Date: 2/2/2013
#Notes:
Created this file to act as a remote control from my pc to my computer!


"""

"""
try:
    import serial
    print 'Serial Imported'
except:
    import testserial as serial
    pass
"""
#import testserial as serial
import serial
    
import binascii
import threading
import Queue
import string
import time

from Tkinter import *
import ttk


"""
ser = serial.Serial('COM1', timeout=4)
ser.baudrate = 9600

print ser.portstr

array = 'ka 00 1\x0D'
print 'Send'
print 'Ascii Data: ', array
print 'Raw Data:   ', binascii.hexlify(array)

ser.write(array)

x = ser.read(100)
print 'Receive'
print 'Ascii Data: ', x
print 'Raw Data:   ', binascii.hexlify(x)

ser.close()
"""

class lgtv(object):
    def __init__(self, comPort='COM0', setID='00'):
        self.comPort = comPort
        print 'Opening serial connection on: ', comPort
        self.setID = setID
        self.alive = True
        
        #Open serial port
        self.__ser = serial.Serial(self.comPort, timeout=0.5)
        self.rxThread = threading.Thread(None, target=self.__rx__)
        self.rxThread.start()
        self.rxQueue = Queue.Queue()
        
        self.txThread = threading.Thread(None, target=self.__tx__)
        self.txThread.start()
        self.txQueue = Queue.Queue()
        
        #Current TV state
        self.__power = False
        self.__volume = '00'
        self.__input = '00'
        
    def __del__(self):
        print 'lgtv destructor'
        self.alive = False
        self.txThread.join()
        self.rxThread.join()
        print 'Threads joined now exiting'
    
    def disconnect(self):
        self.__del__()
        
    def __tx__(self):
        print 'Starting transmit thread'
        while self.alive:
            try:
                self.__ser.write(self.txQueue.get(True, 1))
            except:
                pass
        return
        
    def __rx__(self):
        print 'Starting recieve thread'
        while self.alive:
            try:
                self.__ser.read(100)
            except:
                pass
    
    def power(self, on=True):
        if on:
            self.__power = True
            self.txQueue.put(lgMsg(self.setID, 'ka', '1'), False)
        else:
            self.__power = False
            self.txQueue.put(lgMsg(self.setID, 'ka', '0'), False)
        return
        
    
        
class lgMsg(object):
    """
    Class: lgMsg
    creates a message to send to an lg tv
    helper class
    """
    def __init__(self, setID='00', command='ka', data='FF'):
        self.__setID = setID
        self.__command = command
        self.__data = data
        self.msg = self.updateMsg()
    
    def __str__(self):
        return self.msg
    
    def __repr__(self):
        return self.msg
        
    def updateMsg(self):    
        self.msg = string.join([self.__command, 
                                ' ',
                                self.__setID,
                                ' ',
                                self.__data,
                                '\x0D'],
                                '')
        return self.msg
    
if __name__ == '__main__':
    tv = lgtv('COM1')
    
    root = Tk()
    root.title('TV Remote')
    powerButtonOn = ttk.Button(root, text="Power On", command=lambda: tv.power(True))
    powerButtonOff = ttk.Button(root, text="Power On", command=lambda: tv.power(False))
    powerButtonOn.grid(column=0, row=0)
    powerButtonOff.grid(column=0, row=1)
    root.mainloop()
    
    tv.disconnect();