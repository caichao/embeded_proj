import threading
from time import sleep,ctime
import RPi.GPIO as GPIO

red = 16
green = 20
blue = 21

def initPin():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red,GPIO.OUT,initial=GPIO.OUT)
    GPIO.setup(green,GPIO.OUT,initial=GPIO.OUT)
    GPIO.setup(blue,GPIO.OUT,initial=GPIO.OUT)

    GPIO.output(red,1)
    GPIO.output(green,1)
    GPIO.output(blue,1)

def toggleLed(channel):
    GPIO.output(channel,0)
    sleep(1)

    GPIO.output(channel,1)
    sleep(1)

def flashLed(channel):
    GPIO.output(channel,0)
    sleep(0.08)

    GPIO.output(channel,1)
    sleep(1)

def main():
    initPin()
    while True:
        toggleLed(red)
        toggleLed(green)
        toggleLed(blue)
        flashLed(red)
        flashLed(green)
        flashLed(blue)

if __name__ == '__main__':
    try:
        main()
    except:
        GPIO.cleanup()
        print('clean up the gpio')
