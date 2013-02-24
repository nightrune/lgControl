"""

#Author: Sean Sill
#email: sms3h2@gmail.com
#Date: 2/2/2013
#Notes:
Created this file to act as a remote control from my pc to my computer!


"""


try:
    import serial
    print 'Serial Imported'
except:
    import testserial as serial
    pass
    
#import testserial as serial
#import serial
    
import xml.dom.minidom
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
    def __init__(self, file='', comPort='COM0', setID='00'):
        self.inputs = {}
        self.alive = False
        
        if(file != ''):
            self.__importSettings(file)
            self.comPort = comPort
            self.setID = setID
        else:            
            self.comPort = comPort
            self.setID = setID
        
        print 'Opening serial connection on: ', comPort
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
    
    def __importSettings(self, file):
        if self.alive:
            raise Exception('Can not try to import settings during runtime!!')
        try:
            print "Attempting to open file"
            dom = xml.dom.minidom.parse(file)
            #Now to parse the file
            for node in dom.getElementsByTagName('input'):
                print node
                name = node.getAttribute('name')
                if(name != ''):
                    data = node.childNodes[0].data
                    self.inputs[name] = data
            
        except:
            print "Invalid Config File"
            quit()
        print "Imported config file"
        return
        
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
        
    def input(self, inputString):
        """
        Takes a string and updates the input via the string.
        This hasn't been completely updated yet, and really needs a way to load in a 
        text file that allows you to set the values
        """
        if(self.inputs.has_key(inputString)):
            self.txQueue.put(lgMsg(self.setID, 'xb', self.inputs[inputString]), False)
    
        
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
    #Load configuration files
    tv = lgtv('config.xml', 'COM1')
    
    root = Tk()
    root.title('TV Remote')
    inputButtons = []
    powerButtonOn = ttk.Button(root, text="Power On", command=lambda: tv.power(True))
    powerButtonOff = ttk.Button(root, text="Power Off", command=lambda: tv.power(False))
    for key in tv.inputs:
        inputButtons.append(ttk.Button(root, text=key, command = lambda x = key: tv.input(x)))
    #Grid the buttons
    powerButtonOn.grid(column=0, row=0)
    powerButtonOff.grid(column=0, row=1)
    for i in range(len(inputButtons)):
        inputButtons[i].grid(column=0, row=(2+i))
    
    root.mainloop()
    
    tv.disconnect();