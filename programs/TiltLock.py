# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import board
import adafruit_lis3dh
import busio
import neopixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()
 
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

def getLocation(accel):
    """
    This function returns the current orientation with the values
    (Orientation is facing the playground with the USB in back)
    All directions are the direction when that 
    0 - Left (ie left side on Bottom)
    1 - Inward (USB on Top)
    2 - Flat
    3 - Right (R side on Bottom)
    4 - Outward (USB on Bottom)
    5 - Upside Down (Buttons down)  
    
    returns None if accelration is too high or max value not close to one directions
    """
    absAccel = [abs(a) for a in accel]
    maxVal = max(absAccel)
    if sum(absAccel)>11.5 or maxVal<7: #Shaking or wrong angle
        return()
    else:
        argIdx = [i for i in range(len(accel)) if accel[i]==maxVal][-1]
        if accel[argIdx]<0:
            return(argIdx+3)
        else:
            return(argIdx)
        
def checkPattern(sequence = (0,3,0,1,4), numOfOccurances = 3):
    """
    This function will take in the specific squence that needs to be done to open the lock
    Locations 2 and 5 (which are flat and upsidedown) don't currently count as locations
    The number of occurances is the number of times the same position must be measured to count it
        - This will hopefully address issues with shaking it or knocking on it etc
    """
    prevLoc = [i for i in range(0,-numOfOccurances,-1)] #Lists previous location measurements, negatives to prevent assignment
    seq=[-1 for _ in sequence]
    while seq!=sequence:
        pixels.fill((255, 0, 0))
        while not all([nLoc==prevLoc[0] for nLoc in prevLoc[1:]]) :
            pixels.fill((255, 0, 0))
            pixels.show()
            time.sleep(0.1)
            loc = getLocation(lis3dh.acceleration[:])
            prevLoc=[i for i in prevLoc[1:]].append(loc)
        pixels.fill((0, 0, 255))
        pixels.show()

        if loc not in (2,5,seq[-1]): #Ignore the home position and upsidedown and the same positions as before
            seq= [i for i in seq[1:]].append(loc)    
    return()

def unlock(time=5):
    """Write to a pin a positive 5V for period of "time" seconds"""
    return()

def flash_pixels(flash_speed=0.5):
    print('flashing R')
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(flash_speed)
    
    print('flashing G')
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(flash_speed)
    
    print('flashing B')
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(flash_speed)



def main():
    flash_pixels()
    pixels.fill((0, 0, 0))
    pixels.show()
  
    while True:
        checkPattern(sequence=(0,3,0))
        unlock()
        
        for i in range(20):
            flash_pixels()

main()
