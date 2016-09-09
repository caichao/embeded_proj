#coding=utf-8

#----------------------------------import area----------------------------------------------------

#import httplib2
import requests
import threading
from time import ctime,sleep

#-----------------------------------global var--------------------------------------------------------------

URL = "http://localhost:8080/IoT/servlet/IoTServlet"

#-----------------------------------class area----------------------------------------------------
class MyThread(threading.Thread):
    ''' a user defined multi-thread class '''
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        
    def getResult(self):
        return self.res
    
    def run(self):
        self.res = apply(self.func,self.args)
        



#------------------------------------function area---------------------------------------------------

    
def uploadSensorInfo():
    while True:
        temperature = 35
        humidity = 35.6
        lumiance = 44
        url = URL
        parmeters = {'humidity':humidity,'temperature':temperature,'lumiance':lumiance,'requestType':'sensor'}
        r = requests.get(url,params = parmeters)
        print (r.url)
        print (r)
        print (r.text)
        sleep(1)

def uploadPicture():
    while True:
        url = URL+"?requesType=image"
        file = {'file':open('a.png','rb')}
        r = requests.post(url,files=file)
        print (r)
        print (r.url)
        print (r.text)
        sleep(1)

def main():
    #thread1 = MyThread(uploadSensorInfo,(123,324,435))
    #thread2 = MyThread(uploadPicture,())
    #thread1.start()
    #thread2.start()
    
    t1 = threading.Thread(target = uploadSensorInfo)
    t2 = threading.Thread(target = uploadPicture)
    t1.start()
    t2.start()
    print("thread started")
    while True:
        pass
    print("Thread over")
if __name__ == '__main__':
    #main()
    #print(getUploadedUrl(35.2,24.2,54.23))
    #uploadPicture()
    #uploadSensorInfo(35,234,345)
    main()
