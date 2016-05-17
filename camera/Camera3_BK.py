
import os
import datetime
import time

import traceback
from time import sleep
import sys

import socket
import flickrapi
import webbrowser




#!/usr/bin/env python
# created by chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2015/05/22/raspberry-pi-and-flickr/

testServer = 'www.google.com'

########################
### Variables Config ###
########################

api_key = u'f87473f93a9ed6a05d0da74e9efb8817' 
api_secret = u'15383594491a2e38' 

def CAM():
	t=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	file = '/home/pi/Desktop/Picode/camera/images/MyGarden'+t+'.jpg'
	print(file)
	if (int(datetime.datetime.now().strftime("%H")) >= 21 or int(datetime.datetime.now().strftime("%H")) < 6):
		os.system("raspistill -a 12 -ss 6000000 -awb off -awbg 1,1 -ISO 800 -t 60000 -o "+file+"")
	if (int(datetime.datetime.now().strftime("%H")) >= 6 or int(datetime.datetime.now().strftime("%H")) < 7):  
		os.system("raspistill -a 12 -ss 6000000 -awb off -awbg 1,1 -ISO 400 -t 60000 -o "+file+"")
	if (int(datetime.datetime.now().strftime("%H")) >= 7 and int(datetime.datetime.now().strftime("%H")) < 17):
		os.system("raspistill -a 12 -o "+file+"")
	
	#os.system("raspistill -a 12 -o "+file+"")
		
	
	print("now to copy to website")	
	os.system("cp "+file+" /var/www/Garden.png")
	connected = isConnected()
	if (connected == True):
		print("Delete File To Save Disk Space")		
		os.system("rm "+file+"")

	print("now to copy to Flickr")	
	uploadToFlickr('/var/www/Garden.png',t)


def toUnicodeOrBust(obj, encoding='utf-8'):
	   if isinstance(obj, basestring):
		 if not isinstance(obj, unicode):
			 obj = unicode(obj, encoding)
	   return obj

def isConnected():
	 try:
		 # see if we can resolve the host name -- tells us if there is a DNS listening
		 host = socket.gethostbyname(testServer)
		 # connect to the host -- tells us if the host is actually reachable
		 s = socket.create_connection((host, 80), 2)
		 return True
	 except:
		  pass
	 return False 	


def uploadToFlickr(file,tag):
	flickr = flickrapi.FlickrAPI(api_key, api_secret)

	print('Step 1: authenticate')

	# Only do this if we don't have a valid token already
	if not flickr.token_valid(perms=u'write'):

		# Get a request token
		print('1')	
		flickr.get_request_token(oauth_callback='oob')
		print('2')
		# Open a browser at the authentication URL. Do this however
		# you want, as long as the user visits that URL.
		authorize_url = flickr.auth_url(perms=u'write')
		print('3')
		webbrowser.open_new_tab(authorize_url)
		print('4')	
		# Get the verifier code from the user. Do this however you
		# want, as long as the user gives the application the code.
		verifier = toUnicodeOrBust(raw_input('Verifier code: '))
		print('5')
		# Trade the request token for an access token
		flickr.get_access_token(verifier)
	
	print('6')
	flickr.upload(filename=file, tags=tag)
	print('7')




if __name__ == '__main__': #Program starting from here
        CAM()


