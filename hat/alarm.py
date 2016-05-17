from sense_hat import SenseHat
import time

sense = SenseHat()

w = [150,150,150]
b = [0,0,255]
e = [0,0,0]
R = [255,0,0]

image = [
    e,R,R,R,R,R,R,e,
    R,e,R,R,R,R,e,R,
    R,R,e,R,R,e,R,R,
    R,R,R,e,e,R,R,R,
    R,R,R,e,e,R,R,R,
    R,R,e,R,R,e,R,R,
    R,e,R,R,R,R,e,R,
    e,R,R,R,R,R,R,e
]

image2 = [
    e,b,b,b,b,b,b,e,
    b,e,b,b,b,b,e,b,
    b,b,e,b,b,e,b,b,
    b,b,b,e,e,b,b,b,
    b,b,b,e,e,b,b,b,
    b,b,e,b,b,e,b,b,
    b,e,b,b,b,b,e,b,
    e,b,b,b,b,b,b,e
]

while True:
    time.sleep(1)
    sense.set_pixels(image)
    time.sleep(1)
    sense.set_pixels(image2)
