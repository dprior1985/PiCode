from sense_hat import SenseHat
import random
sense = SenseHat()





def loop():
    i = 0
    y = 20

    while (i <= y):
        r = random.randint(0,255)
        b = random.randint(0,255)
        g = random.randint(0,255)
	
        r1 = random.randint(0,255)
        b1 = random.randint(0,255)
        g1 = random.randint(0,255)
        sense.show_message("Happy New Year!!!!", scroll_speed=0.05, text_colour=[r,g,b], back_colour=[r1,g1,b1])
        print(i,'rgb text' ,r,g,b,'rgb back',r1,g1,b1)
        i = i+1




if __name__ == '__main__': #Program starting from here
    try:
        loop()
        sense.clear() 
    except KeyboardInterrupt: 
        sense.clear()