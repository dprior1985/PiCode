
import picamera
import datetime
import os
import time
from time import sleep
camera = picamera.PiCamera()



camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.resolution=(1280,720)
camera.ISO = 100
camera.shutterspeed=6000000
camera.video_stabilization = False
camera.exposure_compensation = -10
camera.exposure_mode = 'night'

camera.meter_mode = 'average'
camera.awb_mode = 'off'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

t=datetime.datetime.now().strftime("%Y%m%d%H%M%S")

file = '/home/pi/Desktop/Picode/camera/images/MyGarden'+t+'.jpg'
print(file)
sleep(1)
camera.capture(file)
