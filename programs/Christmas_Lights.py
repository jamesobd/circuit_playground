# Circuit Playground NeoPixel
import time
import board
import neopixel

def movingPix(start,stop,color, delay):
    prevColor = pixels[start]
    print(prevColor)
    step = 1
    if start>stop:
        step = -1
    for i in range(start, stop):
        print(i,step)
        if i == start:
            pixels[i] = color
            pixels.show()
            time.sleep(delay)
        else:
            pixels[i] = color
            pixels[i-step] = prevColor
            pixels.show()
            time.sleep(delay)
    return()



pixCount = 50
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
startColor = WHITE

pixels = neopixel.NeoPixel(board.A1, pixCount, brightness=1, auto_write=False)

# choose which demos to play
# 1 means play, 0 means don't!
color_chase_demo = 1
flash_demo = 1
rainbow_demo = 1
rainbow_cycle_demo = 1

#Start with specific color filled (or none)
pixels.fill(startColor)
pixels.show()

#movingPix(0, pixCount, RED, 0.5)

#Start looping up colors
for travellingColor in (RED,BLUE,GREEN):
    for i in range(pixCount,0,-1):
        movingPix(0, i, travellingColor, 0.05)
