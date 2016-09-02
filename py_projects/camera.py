from picamera import PiCamera
from time import sleep

camera=PiCamera()

#-----------video preview on the HDMI output-------------

#camera.start_preview()
#sleep(10)
#camera.stop_preview()

#print('video stream stopped')
#leep(2)


#-----------capture a picture and save it-----------------
camera.start_preview()
print('begin to start preview')
sleep(5)
camera.capture('/home/pi/Desktop/image.jpg')
print('capture a picture and flush it on the desktop')
camera.stop_preview()


#-----------capture a video and save it ------------------
print('begin to capture a vedio stream')
camera.start_preview()
camera.start_recording('/home/pi/video.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview();
print('vedio stream capture end')



