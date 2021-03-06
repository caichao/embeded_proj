#!/usr/bin/env python
#system package
import threading
import time
import os
import socket
import json

#------------------------custom package----------------------------
import bh1750
import led
import database as db
import log

#------------------------global var--------------------------------

global g_temperature,g_humidity,g_lumiance

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

class LedBlinkThread(threading.Thread):
    '''a led blink thread which indicate the program is normally running'''
    def __init__(self,color):
        threading.Thread.__init__(self)
        self.color = color

    def run(self):
        while True:
            led.toggle(self.color)
            time.sleep(0.5)

class MultipackageSendThread(threading.Thread):
    '''tcp channel to send all the sensor information in the database'''
    def __init__(self,host,port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        address = (self.host,self.port)
        tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp.bind(address)
        tcp.listen(10)
        tcp_channel,tcp_addr = tcp.accept()
        timeList,temperatureList,humidityList,lumianceList = db.queryListResult()
        for i in range(len(timeList)):
            str_sensor = strSensorInfo(timeList[i],temperatureList[i],humidityList[i],lumianceList[i])
            tcp_channel.send(str_sensor.encode('utf-8'))
        tcp_channel.close()
        tcp.close()
        
class BroadcastServerThread(threading.Thread):
    '''a udp server'''
    #host = ''
    #port = 10000
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,10)
    
    latest_sensor = b'LATEST_SENSOR'
    all_sensor = b'ALL_SENSOR'
    def __init__(self,host = '',port=10000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.s.bind((host,port))
    def run(self):
        while True:
            ack,addr = self.s.recvfrom(1024)
##            print('data from client:',addr)
            #parse the request from the client
            if ack == self.latest_sensor:
                print('fetch latest')
                time,temperature,humidity,lumiance = db.queryLatestResult()
                
                str_sensor = jsonSensorInfo(time,temperature,humidity,lumiance)
                self.s.sendto(str_sensor.encode('utf-8'),addr)
                print('already send the sensor information')
                #print (ack)
            elif ack == self.all_sensor:
                print('fetch all')
                timeList,temperatureList,humidityList,lumianceList = db.queryListResult()
##                number_of_records = str.format('records=%d' % len(timeList))
                number_of_records = {}
                number_of_records['records'] = len(timeList)
                json_num = json.dumps(number_of_records)
                self.s.sendto(json_num.encode('utf-8'),addr)
                # if use udp here, package loss will be great, so we use tcp instead
                # addr here contains both host address and  ports

##                t = MultipackageSendThread(addr[0],50000)
##                t.setDaemon(True)
##                t.start()
##                address = (addr[0],self.port-1)
##                tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##                tcp.bind(address)
##                tcp.listen(10)
##                tcp_channel,tcp_addr = tcp.accept()
##        
                for i in range(len(timeList)):
                    str_sensor = jsonSensorInfo(timeList[i],temperatureList[i],humidityList[i],lumianceList[i])
                    self.s.recvfrom(50)  #echo the ack information
                    self.s.sendto(str_sensor.encode('utf-8'),addr)
                    #self.s.recvfrom(50)
##                    print('i = ',i)
##                    tcp_channel.send(str_sensor.encode('utf-8'))
##
##                tcp_channel.close()
##                tcp.close()
                print ("all the sensor information has been sent")
            else:
                print('can not parse message')
            #print("ack = ",ack)
            #str_sensor = strSensorInfo(temperature,humidity,lumiance)
            #self.s.sendto(str_sensor.encode('utf-8'),addr)            

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
##        print('temperature = %.02f \n humidity = %.02f' %(temperature,humidity))
        return temperature,humidity
    except:
        print('get temperature & humidity error')
        log.recordError(log.DHT11ERR)
##        temperature = None
##        humidity = None
        return None,None

def getLumiance():
    ''' get the lumiance from the drive '''
    try:
        lumiance = bh1750.readLight()
##        print('lumiance = %.02f' % lumiance)
    except:
        print('read lumiance error')
        lumiance = None
        log.recordError(log.BH1750ERR)
    return lumiance
def jsonSensorInfo(time,temperature,humidity,lumiance):
    json_str = {}
    json_str['temperature'] = temperature
    json_str['humidity'] = humidity
    json_str['lumiance'] = lumiance
    json_str['time'] = time

    return json.dumps(json_str)

def strSensorInfo(time,temperature,humidity,lumiance):
    '''sensor information in str'''
    temperature = float(temperature)
    humidity = float(humidity)
    lumiance = float(lumiance)
    return ("time = %s|temperature = %.02f|humidity = %.02f|lumiance = %.02f|" %(time,temperature,humidity,lumiance))


def main():
    ''' main function '''

    #set a broadcasting thread
    broadcast_thread = BroadcastServerThread()
    broadcast_thread.setDaemon(True)
    broadcast_thread.start()

    #a led blink thread
##    blink_thread = LedBlinkThread(led.blue)
##    blink_thread.setDaemon(True)
##    blink_thread.start()

    print('Program started successfully')
    while True:

        try:
            g_temperature,g_humidity = getTemperatureHumidity()
            g_lumiance = getLumiance()
            led.flash(led.green)

            if g_temperature != None and g_humidity != None and g_lumiance != None:
                db.insertSensorValue(g_temperature,g_humidity,g_lumiance,'home')

##            time.sleep(60)
            for i in range(60):
                led.toggle(led.blue)
                time.sleep(1)
        except:
            print('Program exit with exception')
            raise


if __name__ == '__main__':
    main()
