from copy import deepcopy
import time

class Serial(object):
    def __init__(self, port=None, 
                    baudrate=9600, 
                    bytesize=8, 
                    partiy=None,
					stopBits=1,
					timeout=0,
                    xonxoff=False,
                    rtscts=False,
                    writeTimeout=None,
                    dsrdtr=False,
                    interCharTimeout=None):
        print 'Dummy Port'
        self.timeout = timeout
        self.baudrate = baudrate
        self.portstr = 'Dummy'
        self.dummyData = ''
		
    def write(self, data):
        self.dummyData = deepcopy(data)
        print 'Dummy write: ', data
		
    def read(self, size):
        data = ''
        time.sleep(self.timeout)
        if(size > self.dummyData.__len__()):
            size = self.dummyData.__len__()
        
        if(size > 0):
            data = self.dummyData[:size]
            self.dummyData = ''
            print 'Dummy read: ', data
        return data
    
    def close(self):
        print 'Dummy port closed'