#!/usr/bin/evn python

import sqlite3
import threading
#import matplotlib.pyplot as plt
#import numpy as np

lock = threading.Lock()
#--------------------------------function-----------------------------
def queryResults():
    lock.acquire()
    conn = sqlite3.connect('sensor.db')
    cursor = conn.cursor()
    row = cursor.execute('select *  from sensor_table')
    values = cursor.fetchall()
    print('number of queried results:',len(values))
    print('result:',values)
    cursor.close()
    conn.close()
    lock.release()
    return values

def queryListResult(location="home"):
    
    lock.acquire()
    conn = sqlite3.connect('sensor.db')
    cursor = conn.cursor()
    sql = str.format('select temperature,humidity,lumiance from sensor_table where location="%s"' % location)
    row = cursor.execute(sql)
    values = cursor.fetchall()
    print('number of queried results:',len(values))
    print('result:',values)
    cursor.close()
    conn.close()
    lock.release()
    
    temperatureList = []
    humidityList = []
    lumianceList = []
    
    for item in values:
        temperatureList.append(item[0])
        humidityList.append(item[1])
        lumianceList.append(item[2])
    return temperatureList,humidityList,lumianceList

def queryLatestResult():
    lock.acquire()
    conn = sqlite3.connect('sensor.db')
    cursor = conn.cursor()
    cursor.execute('select *  from sensor_table order by tdatetime desc')
    values = cursor.fetchone()
    #print('number of queried results:',)
    print('result:',values)
    cursor.close()
    conn.close()
    lock.release()
    return values

def insertSensorValue(temperature,humidity,lumiance,location):
    lock.acquire()
    conn = sqlite3.connect('sensor.db')
    cursor = conn.cursor()
    cursor.execute('insert into sensor_table(temperature,humidity,lumiance,location) values(?,?,?,?)',(temperature,humidity,lumiance,location))
    conn.commit()
    cursor.close()
    conn.close()
    lock.release()

def deleteAllSensorValue():
    lock.acquire()
    conn = sqlite3.connect('sensor.db')
    cursor = conn.cursor()
    cursor.execute('delete from sensor_table')
    conn.commit()
    cursor.close()
    conn.close()
    lock.release()


if __name__ == '__main__':
    #insertSensorValue(23.1,32.4,23,'home')
    #queryResults()
    #queryLatestResult()
    tlist,hlist,llist = queryListResult()
    print(tlist)
    print(hlist)
    print(llist)
