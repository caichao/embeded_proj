import threading
import time
import os

import bh1750

def getTemperatureHumidity():
    ret = os.popen('sudo /usr/local/bin/Adafruit_DHT 2302 23').read()
    cell = ret.split('=')
    temperature = cell[1].split('*')
    temperature = temperature[0]
    humidity = cell[2].split('%')
    humidity = humidity[0]
    print('temperature = '+temperature + 'humidity=' + humidity)
    return temperature,humidity

def getLumiance():
    lumiance = bh1750.readLight()
    print('lumiance = '+str(lumiance))
    return lumiance

def main():
    getTemperatureHumidity()
    getLumiance()


if __name__ == '__main__':
    main()
