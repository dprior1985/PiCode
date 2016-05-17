from sense_hat import SenseHat
import time

sense = SenseHat()

w = [150,150,150]
b = [0,0,255]
e = [0,0,0]

image = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    w,w,w,e,e,b,b,b,
    w,w,w,e,e,b,b,b,
    w,w,w,e,e,b,b,b,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
]

sense.set_pixels(image)

while True:
    time.sleep(1)
    sense.flip_h()
