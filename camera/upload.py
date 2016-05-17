#!/usr/bin/env python
# created by chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2015/05/22/raspberry-pi-and-flickr/

import os

import time
import traceback
from time import sleep
import sys

import socket
import flickrapi
import webbrowser

########################
### Variables Config ###
########################

api_key = u'47fb816c210ab3689ca686a7a1a424f2' 
api_secret = u'70612e036f5cf186' 

def toUnicodeOrBust(obj, encoding='utf-8'):
	   if isinstance(obj, basestring):
		 if not isinstance(obj, unicode):
			 obj = unicode(obj, encoding)
	   return obj


def uploadToFlickr(file,tag):
	flickr = flickrapi.FlickrAPI(api_key, api_secret)
	print('Step 1: authenticate')
	# Only do this if we don't have a valid token already
	
	if not flickr.token_valid(perms=u'write'):
		# Get a request token
		flickr.get_request_token(oauth_callback='oob')
		# Open a browser at the authentication URL. Do this however
		# you want, as long as the user visits that URL.
		authorize_url = flickr.auth_url(perms=u'write')
		webbrowser.open_new_tab(authorize_url)
		# Get the verifier code from the user. Do this however you
		# want, as long as the user gives the application the code.
		verifier = toUnicodeOrBust(raw_input('Verifier code: '))
		# Trade the request token for an access token
		flickr.get_access_token(verifier)
	
	print "File Start upload"
	flickr.upload(filename=file, tags=tag)
	print "File uploaded"
	

def main():
	uploadToFlickr("/home/pi/Desktop/Picode/camera/test.jpg","test1")






if __name__ == '__main__':
	main()
