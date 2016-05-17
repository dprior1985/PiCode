#Simple meteorology
 
from sense_hat import SenseHat
import time

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
   
        sense.show_message(msg,scroll_speed=0.05)
        time.sleep(60)
   


if __name__ == '__main__': #Program starting from here
    try:
        loop()
        sense.clear() 
    except KeyboardInterrupt: 
        sense.clear()