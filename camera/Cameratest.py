
import os
import datetime
import time

def CAM():
	t=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	file = '/home/pi/Desktop/Picode/camera/images/MyGarden'+t+'.jpg'
	print(file)
	os.system("raspistill -a 12 -o "+file+"")
		
	

	

if __name__ == '__main__': #Program starting from here
    try:
        CAM()
    except KeyboardInterrupt: 
        sense.clear()

