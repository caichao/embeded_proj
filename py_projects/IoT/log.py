import time
import json
import socket


#-----------------------------global var----------------------
DHT11ERR = 'DHT11'
BH1750ERR = 'BH1750'
URL = "http://city.ip138.com/ip2city.asp"
LOC_URL = "http://ip.taobao.com/service/getIpInfo.php?ip="

#-----------------------------class area----------------------

#-----------------------------function area-------------------
def recordError(type):
    with open('log.txt','a+') as f:
        error = str.format('read %s sensor encounter error at:' % type)
        f.write(error)
        f.write(time.asctime(time.localtime(time.time())))
        f.write('\n')
        f.close()
def location():
    pass

def getIP():
    try:
        ret = os.popen('curl ifconfig.me').read()
        return ret
    except:
        raise
    

def main():
    recordError(DHT11ERR)
##    recordError()
##    getIP()
##    r = requests.get(url = (LOC_URL+"183.93.85.188"))
##    data = r.text["data"]1is
##    print(data["country"])
##    print(data["area"])
##    print(data["region"])

if __name__ == '__main__':
    main()
