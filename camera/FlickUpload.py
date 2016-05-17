


#time setup
import time

#for the cp command
import os
import os.path

#setup for datestamping folders
import time

#Flickr Setup
import flickrapi

api_key = 'f87473f93a9ed6a05d0da74e9efb8817'
api_secret = '15383594491a2e38'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json') 
(token, frob) = flickr.get_token_part_one(perms='write')


#Storage Locations
sdcard = '/home/pi/Desktop/Picode/camera/images'
destination = '/home/pi/Desktop/Picode/camera/images/done'


#these functions will be filled later, but right now it's just a simple led blink
def flickr_upload():
	print "Uploading Photos To Flickr"

	
	
	flickr_number = 0
	
	flickr_upload_list = []

	for path, subdirs, files in os.walk(sdcard):
		for filename in files:
			listfiles = os.path.join(path, filename)
			upload_response = flickr.upload(filename = listfiles, format='etree')
			upload_ID = upload_response.find('photoid').text
			flickr_upload_list.insert(flickr_number,upload_ID)
			
			print 'Photo ' + str(flickr_number) + ' uploaded' + ' ID: ' + upload_ID + ' : ' + str(flickr_upload_list[flickr_number])
			flickr_number = flickr_number + 1
	
	set_name = 'Uploaded At ' + time.strftime('%m-%d-%y_%H-%M-%S')
	
	print 'Creating Set: ' + set_name
	
	json_string = flickr.photosets_create(title=set_name, primary_photo_id=flickr_upload_list[0])
	set_id = json_string.split('"')[5]
	
	print 'Set Created: ' + set_id
	print 'Adding Files To list'
	
	for s in flickr_upload_list:
		flickr.photosets_addPhoto(photoset_id=set_id, photo_id=s)
		print 'Photo: ' + s + ' Added To Set: ' + set_id
	

	print "Flickr Upload Completed"



def main():
	flickr_upload()

	
	
if __name__ == '__main__':
		main()
	