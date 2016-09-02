#!usr/bin/python
from tsl2561 import TSL2561
import time

def main():
    try:
        tsl = TSL2561(debug=1)
        while True:
            #tsl = TSL2561()
            print ('lummiance = %d lux' % tsl.lux())
            time.sleep(1)
    except Exception,err:
        print Exception,err
if __name__=="__main__":
    main()
