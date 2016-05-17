#Version 1.0
# 31/08/2015 - danny prior
# this script will allow for a automated garden water system which uses senors to determine what needs to be watered


import urllib2
import json
import RPi.GPIO as GPIO
import time
import MySQLdb
import datetime
import os
import sys

sys.path.append('/home/pi/Desktop/modules')

import lightsensor
import openrelay
import TemperatureSenor
import WeatherAPI
		
		
# Open database connection
db = MySQLdb.connect("localhost","danny","danny123","MYGARDEN" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
Weather1 ="";
RunNumber = 0;
Water = 0;
cnt = 0;
icon_url = "";

#GPIO PINS SETUP
GPIO.setmode(GPIO.BOARD)

watertest = 40; # GPIO pin number
GPIO.setup(watertest,GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #PUD_DOWN pulls down GPIO from third state (random) to 2 state pin (true or false). found this out as results where coming back random


Rain = 11; # GPIO pin number
GPIO.setup(Rain,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)




insert ="INSERT INTO ControlLog(LogDescription,ActionName,SaveData,ControlId,DateNow)";
sql3 = "";		

def main():

		
	global Water;
		
	
	print "light classmethod"
	print(datetime.datetime.now())
	light()
	print(datetime.datetime.now())
	


	print "END"
	print(datetime.datetime.now())


# disconnect from server
	db.close()

def light():
	print("33 start")
	light1 = lightsensor.RCtime(33)
	print("33 end")
#	light2 = lightsensor.RCtime(36)
	sql1 =  insert +" values('light sensor','light sensor 1','%s',1,now() );" % light1   
#	sql2 =  insert +" values('light sensor','light sensor 2','%s',1,now() );" % light2  
	
	# Execute the SQL command
  	cursor.execute(sql1)
	print sql1
#	cursor.execute(sql2)
	
def temperature():
	

	temperature1 =	TemperatureSenor.Sensor("28-0115524404ff")
	temperature2 =	TemperatureSenor.Sensor("28-031553a54dff")
	temperature3 =	TemperatureSenor.Sensor("28-031553aaf4ff")
	temperature4 =	TemperatureSenor.Sensor("28-031553aca3ff")
	temperature5 =	TemperatureSenor.Sensor("28-031553b046ff")

	sql1 =  insert +" values('temp sensor','temp sensor 1','%s',1,now() );" % temperature1   
	sql2 =  insert +" values('temp sensor','temp sensor 2','%s',1,now() );" % temperature2  
	sql3 =  insert +" values('temp sensor','temp sensor 3','%s',1,now() );" % temperature3
	sql4 =  insert +" values('temp sensor','temp sensor 4','%s',1,now() );" % temperature4 
	sql5 =  insert +" values('temp sensor','temp sensor 5','%s',1,now() );" % temperature5  

 
	# Execute the SQL command
  	cursor.execute(sql1)
	cursor.execute(sql2)
	cursor.execute(sql3)
	cursor.execute(sql4)
	cursor.execute(sql5)



	
def decide():

	global Water;

#if temp < 14 then dont water
	sq53 =  "update RunNumber set Water = 0 where Water > 0 and  RunnumberId in (select RunNumberId from ControlLog where SavedDataInt < 14 and Active = 1 ) and RunNumberId = %s ;" %  (int(RunNumber))
	
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with temp <14 "
	   	db.rollback()

#if API says raining then dont water	
	sq53 =  "update RunNumber set Water = -1 where Water > 0 and RunnumberId in (select RunNumberId from ControlLog where LogDescription = 'Weather' and Active = 1 and (SaveData Like '%%Rain%%' or SaveData Like '%%rain%%') ) and RunNumberId = %s ;" %  (int(RunNumber))
	
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with API raining"
	   	db.rollback()




#if local senor says raining then dont water	
	sq531 =  "update RunNumber set Water = -2 where Water > 0 and  RunnumberId in (select RunNumberId from ControlLog where (ActionName like '%%Rain%%' or ActionName like '%%rain%%' ) and Active = 1 and SaveData = 'Yes' ) and RunNumberId = %s ;" %  (int(RunNumber))
	
	try:
	   # Execute the SQL command
   		cursor.execute(sq531)
	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with local rain senor"
	   	db.rollback()



#if water not exists water
	sq53 =  "update RunNumber set Water = 2 where Water <= 0 and  RunnumberId in (select RunNumberId from ControlLog where ActionName = 'WaterExists' and Active = 1 and SaveData = 'No' ) and RunNumberId = %s ;" %  (int(RunNumber))
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with water not exists"
	   	db.rollback()


#if before 6am or after 9PM dont watar
	sq53 =  "update RunNumber set Water = -3 where  Water > 0 and (hour(now()) >= 21 or hour(now()) <= 5 ) and RunNumberId = %s ;" %  (int(RunNumber))
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with before 6am or 9pm"
	   	db.rollback()


#if not watered in 24 hours water
	sq53 =  "update RunNumber set Water = 3 where Water <= 0 and  RunnumberId in ( select %s from (select distinct RunnumberId from RunNumber where Water = 1 and datediff(now(),DateNow ) = 0 and timestampdiff(HOUR,DateNow,NOW()) <= 24 ) e);" %  (int(RunNumber))
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "-------------"
		print sq53
		print "if not watered in 24 hours water"
	   	db.rollback()
		
#if rained in last 6 hours dont water
	sq53 =  "update RunNumber set Water = -4 where Water > 0 and RunnumberId in ( select distinct %s  from (select distinct RunnumberId from ControlLog where (ActionName like '%%Rain%%' or ActionName like '%%rain%%') and SaveData = 'Yes' and datediff(now(),DateNow ) = 0 and timestampdiff(HOUR,DateNow,NOW()) <= 6 union select distinct RunnumberId from ControlLog where ActionName = 'Weather API' and SaveData Like 'Rain' and datediff(now(),DateNow ) = 0 and timestampdiff(HOUR,DateNow,NOW()) <= 6  ) as e)  ;" %  (int(RunNumber))
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:
		print "-------------"
		print sq53
		print "failure if rained in last 6 hours dont water"
	   	db.rollback()



#if water exists water
	sq53 =  "update RunNumber set Water = -5 where Water > 0 and  RunnumberId in (select RunNumberId from ControlLog where ActionName = 'WaterExists' and Active = 1 and SaveData = 'Yes' ) and RunNumberId = %s ;" %  (int(RunNumber))
	try:
	   # Execute the SQL command
   		cursor.execute(sq53)
	   # Commit your changes in the database
		db.commit()
	except:	
		print "failure with water exists"
	   	db.rollback()

		
	
		

		
		


	cursor.execute("select Water from RunNumber where RunNumberId = %s ;" %  (int(RunNumber)))
	for row in cursor.fetchall():

		Water = (row[0])



def RunNumber():

	sql =  "insert into RunNumber(DateNow,Water)  values(now(),1);"
	
	try:
	   # Execute the SQL command
   		cursor.execute(sql)
	   # Commit your changes in the database
		db.commit()

	except:
	#   # Rollback in case there is any error
	   	print "failure with run number"
		db.rollback()
		
	
	global RunNumber;
	global sql3;

	cursor.execute("select RunNumberID from RunNumber ORDER BY RunNumberId DESC limit 1")
	for row in cursor.fetchall():

		RunNumber = (row[0])
	
	sql3 =  "update ControlLog set RunNumberId = %s ,Active = 1 where RunNumberId is null ;" %  (int(RunNumber))
			
	

def weather():


	try:

		json_string=WeatherAPI.API("geolookup")
		parsed_json = json.loads(json_string)
		# get location
		location = parsed_json['location']['city']
		#get temp
		temp_c = parsed_json['current_observation']['temp_c']
		#get weather	
		#Weather1 = "No Rain";
		Weather1 = parsed_json['current_observation']['weather']
		#if "Rain" in weather: Weather1 = "Rain";
		icon_url = parsed_json['current_observation']['icon_url'];
		

		sql1 = insert +" values('Temp C','Weather API','%s',1,now() );" %  (str(temp_c))
		sql1A = "update ControlLog set SavedDataInt = SaveData where LogDescription = 'Temp C' and SavedDataInt is null "

		sql2 =  insert +" values('Weather','Weather API','%s',1,now() );" %  (str(Weather1)) 
		sql3 =  insert +" values('Icon','Weather API','%s',1,now() );" %  (str(icon_url))
		sql4 =  insert +" values('API Last Update','Weather API','%s',1,now() );" %  (str(parsed_json['current_observation']['observation_time']))
		sql5 =  insert +" values('Temp String','Weather API','%s',1,now() );" %   (str(parsed_json['current_observation']['temperature_string'])) 
		sql6 =  insert +" values('wind_String','Weather API','%s',1,now() );" %   (str(parsed_json['current_observation']['wind_string'])) 



# 
	   # Execute the SQL command
  		cursor.execute(sql1)
		cursor.execute(sql2)
	   	cursor.execute(sql3)
	   	cursor.execute(sql4)
	   	cursor.execute(sql5)
	   	cursor.execute(sql6)
		# Commit your changes in the database
		db.commit()

		cursor.execute(sql1A)
	except:
		print "Failure With Weather API or mySQL DB"	
	   	db.rollback()




def forecastweather():


	try:
		json_string=WeatherAPI.API("forecast")
		parsed_json = json.loads(json_string)
		# get location

		for day in parsed_json['forecast']['simpleforecast']['forecastday']:
			#print day['date']['weekday']
			#print 'conditions '+ day['conditions']

			sql1 = insert +" values('%s','Weather API forecast','%s',1,now() );" %  ("Forecast "+str(day['period']),day['date']['weekday']+": "+day['conditions'])	
			# Execute the SQL command
	  		cursor.execute(sql1)
		
		# Commit your changes in the database
		db.commit()

	except:
		print "Failure With Weather 2 API or mySQL DB"	
	   	db.rollback()



	
def water():

	inputValue = GPIO.input(watertest)
	if (inputValue ==True):

		sql1 = insert +" values('Water','WaterExists','Yes',2,now() );" 
				
	else:			
		sql1 = insert +" values('No Water','WaterExists','No',2,now() );" 
	
	try:
	   # Execute the SQL command
   		cursor.execute(sql1)
   	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with water check"
	   	db.rollback()


def rain():

	inputValue = GPIO.input(Rain)
	if (inputValue ==True):
		sql1 = insert +" values('Raining','Rain','Yes',5,now() );" 
				
	else:
			
		sql1 = insert +" values('Not Raining','Rain','No',5,now() );" 
	
	try:
	   # Execute the SQL command
   		cursor.execute(sql1)
   	   # Commit your changes in the database
		db.commit()
	except:
		print "failure with rain check"
	   	db.rollback()
	


if __name__ == '__main__':
	main()

 	GPIO.cleanup()
