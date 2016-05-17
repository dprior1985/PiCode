#Simple meteorology
 
from sense_hat import SenseHat
import time
import datetime


sense = SenseHat()
cnt = 0
def loop():
    while True :
        pressure = sense.get_pressure()
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        calctemp = 0.0071*temp*temp+0.86*temp-10.0
        calchum=humidity*(2.5-0.029*temp)
        print '%.1f %.1f %.1f' % (pressure, calctemp, calchum)
        msg = "T= %.1f, P=%.1f, H=%.1f" % (calctemp,pressure,calchum)
   
#        sense.show_message(msg,scroll_speed=0.05)
	
	timenow  = datetime.datetime.now()
	
	color = "Lightblue"
	
	website="""
	<!DOCTYPE html>
	<html>
	<head>
	
	<link rel='stylesheet' type='text/css' href='/main.css'>
	<link rel='stylesheet' type='text/css' href='main.css'>
	
	</head>
	<body bgcolour = Lightblue >
	<h2>Pi Sense Hat Sensors</h2>
	<h3>Time:   %s</h3>
	<img src='Garden.png' alt='Graph2' style='width:700px;height:400px;'><br>

	<br>
	
	<p> </p>
	<table style='width:70%%'>
	  <tr>
	    <th>Tempeture (C)</th>
	    <td>%s</td>
	  </tr>
	<p> </p> 
	 <tr>
	    <th>Presure</th>
	    <td>%s</td>
	  </tr>
	  <tr>
	    <th>Humidity</th>
	    <td>%s</td>
	  </tr>
	</table>
	</body>
	</html>
	""" % (
	 timenow
	,calctemp
	,pressure
	,calchum
	)
	
	css="""body {
	    background-color: %s;
	}
	
	h2 {
	    color: navy;
	    margin-left: 20px;
	}
	
	h3 {
	    color: Black;
	    margin-left: 30px;
	}
	
	table, th, td {
	    border: 3px solid black;
	    border-collapse: collapse;
		
	}
	th, td {
	    padding: 5px;
	    text-align: left;
		color:Green
	}
	""" % (
	color
	)
	
	#print website;
	fo = open("/var/www/index.html", "w")
	
	fo.seek(0, 2)
	line = fo.write( website )
	
	# Close opend file
	fo.close()
	
	
	#print css;
	io = open("/var/www/main.css", "w")
	
	io.seek(0, 2)
	line = io.write( css )
	
	# Close opend file
	io.close()

        time.sleep(120)
   


if __name__ == '__main__': #Program starting from here
    try:
        loop()
        sense.clear() 
    except KeyboardInterrupt: 
        sense.clear()