
import os
import datetime
import time

def CAM():
	t=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	file = '/home/pi/Desktop/Picode/camera/images/MyGarden'+t+'.jpg'
	print(file)
	if (int(datetime.datetime.now().strftime("%H")) >= 21 or int(datetime.datetime.now().strftime("%H")) < 6):
		os.system("raspistill -a 12 -ss 6000000 -awb off -awbg 1,1 -ISO 500 -t 60000 -o "+file+"")
	if (int(datetime.datetime.now().strftime("%H")) >= 6 or int(datetime.datetime.now().strftime("%H")) < 7):  
		os.system("raspistill -a 12 -ss 6000000 -awb off -awbg 1,1 -ISO 200 -t 60000 -o "+file+"")
	if (int(datetime.datetime.now().strftime("%H")) >= 7 and int(datetime.datetime.now().strftime("%H")) < 17):
		os.system("raspistill -a 12 -o "+file+"")
		
	#os.system("raspistill -a 12 -o "+file+"")
	print("now to copy to website")	
	os.system("cp "+file+" /var/www/Garden.png")

	

if __name__ == '__main__': #Program starting from here
    try:
        CAM()
    except KeyboardInterrupt: 
        sense.clear()

