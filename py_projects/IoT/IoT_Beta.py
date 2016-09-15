#!/usr/bin/env python
#system package
import threading
import time
import os
import socket

#------------------------custom package----------------------------
import bh1750
import led
import database as db

#------------------------global var--------------------------------



#------------------------class area--------------------------------
class MyThread(threading.Thread):
    '''a user defined multi-thread class'''
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        #self.res = apply(self.func,self.args) #not supported in python3
        #lock.acquire()
        self.res = self.func(*self.args)
        #lock.release()

class BroadcastServerThread(threading.Thread):
    '''a udp server'''
    #host = ''
    #port = 10000
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,10)
    
    latest_sensor = 'LATEST_SENSOR'
    all_sensor = 'ALL_SENSOR'
    def __init__(self,host = '',port=10000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.s.bind((host,port))
    def run(self):
        while True:
            ack,addr = s.recvfrom(1024)
            print('data from client:',addr)
            #parse the request from the client
            if ack == self.latest_sensor:
                print (ack)
            elif ack == self.all_sensor:
                print (ack)
            str_sensor = strSensorInfo(temperature,humidity,lumiance)
            s.sendto(str_sensor.encode('utf-8'),addr)            

#------------------------function area-----------------------------
def getTemperatureHumidity():
    ''' get the temperature from drive '''
    try:
        ret = os.popen('sudo /usr/local/bin/Adafruit_DHT 2302 23').read()
        cell = ret.split('=')
        temperature = cell[1].split('*')
        temperature = temperature[0]
        humidity = cell[2].split('%')
        humidity = humidity[0]
        temperature = float(temperature)
        humidity = float(humidity)
        print('temperature = %.02f \n humidity = %.02f' %(temperature,humidity))
    except:
        print('get temperature & humidity error')
    return temperature,humidity

def getLumiance():
    ''' get the lumiance from the drive '''
    try:
        lumiance = bh1750.readLight()
        print('lumiance = %.02f' % lumiance)
    except:
        print('read lumiance error')
    return lumiance


def ledBlink():
    '''led blink function'''
    while True:
        led.toggle(led.blue)
        time.sleep(1)

def strSensorInfo(temperature,humidity,lumiance):
    '''sensor information in str'''
    return ("temperature = %.02f\n humidity = %.02f \n lumiance = %.02f \n" %(temperature,humidity,lumiance))


def main():
    ''' main function '''

    #set a broadcasting thread
    broadcast_thread = BroadcastServerThread()
    broadcast_thread.setDaemon(True)
    broadcast_thread.start()    
    i = 0
    j = 0
    while j<20:
        try:
            global temperature,humidity,lumiance
            
            temperature,humidity = getTemperatureHumidity()
            lumiance = getLumiance()
            led.flash(led.green)
            if i%10 == 0:
                i = 0
                db.insertSensorValue(temperature,humidity,lumiance,'home')
                print('insert a record')
            i = i + 1 
        except:
            raise


if __name__ == '__main__':
    main()
