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
        self.dummyData = data
        print 'Write: ', data
		
    def read(self, size):
        time.sleep(self.timeout)
        if(size > len(self.dummyData)):
            size = len(self.dummyData)
        print 'Read: ', self.dummyData[:size]
        return self.dummyData[:size]
    
    def close(self):
        print 'Dummy port closed'