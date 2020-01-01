# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import board
import adafruit_lis3dh
import busio
import simpleio
import neopixel
import digitalio
#import mic_utils

# Lock switch setup
lock_switch = digitalio.DigitalInOut(board.D9)
lock_switch.direction = digitalio.Direction.OUTPUT
lock_switch.value = False

# Pixel setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

# Accelerometer setup
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

# Adjust these constants based on the playground's relative orientation
LEFT = 4
INWARD = 2
FLAT = 0
RIGHT = 1
OUTWARD = 5
UPSIDE_DOWN = 3

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

    #New Directions

    5 - Forward (outward)
    4 - left
    2 - backward (inward)
    1 - Right

    returns -1 if accelration is too high or max value not close to one directions
    """
    pixels[0] = (int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)))
    pixels[9] = (int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)), 
                 int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], -1, -9.8, 0, 255)))
    pixels[2] = (int(simpleio.map_range(accel[0], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[0], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[0], 1, 9.8, 0, 255)))
    pixels[4] = (int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)))
    pixels[5] = (int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)),
                 int(simpleio.map_range(accel[1], 1, 9.8, 0, 255)))
    pixels[7] = (int(simpleio.map_range(accel[0], -1, -9.8, 0, 255)),
                 int(simpleio.map_range(accel[0], -1, -9.8, 0, 255)),
                 int(simpleio.map_range(accel[0], -1, -9.8, 0, 255)))

    pixels.show()
    absAccel = [abs(a) for a in accel]
    maxVal = max(absAccel)
    if sum(absAccel) > 11.5 or maxVal < 5:  # Shaking or wrong angle
        return (-1)
    else:
        argIdx = [i for i in range(len(accel)) if absAccel[i] == maxVal][-1]
        if accel[argIdx] < 0:
            return (argIdx + 3)
        else:
            return (argIdx)


def checkPattern(sequence=[LEFT, RIGHT, LEFT], numOfOccurances=2):
    """
    This function will take in the specific sequence that needs to be done to open the lock
    Locations 2 and 5 (which are flat and upside down) don't currently count as locations
    The number of occurrences is the number of times the same position must be measured to count it
        - This will hopefully address issues with shaking it or knocking on it etc
    """
    prevLoc = [i for i in
               range(0, -numOfOccurances, -1)]  # Lists previous location measurements, negatives to prevent assignment
    seq = [-1 for _ in sequence]
    while seq != sequence:
        while not all([nLoc == prevLoc[0] for nLoc in prevLoc[1:]]):
            loc = getLocation(lis3dh.acceleration[:])
            print(loc)
            if loc not in (-1, FLAT, UPSIDE_DOWN, seq[-1]):  #Ignore the flat and upside-down down positions and the previous position
                prevLoc = prevLoc[1:] + [loc]
        seq = seq[1:] + [loc]
        prevLoc[-1] = -1
        print('The current sequence is: {}'.format(seq))


def unlock(delay=5):
    """Write to a pin a positive 3.7V for delay seconds"""
    print('unlocked')
    pixels.fill((0, 255, 0))
    pixels.show()
    lock_switch.value = True

    time.sleep(delay)

    print('locked')
    pixels.fill(0)
    pixels.show()
    lock_switch.value = False


def flash_pixels(flash_speed=0.5):
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(flash_speed)

    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(flash_speed)

    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(flash_speed)


flash_pixels()
pixels.fill((0, 0, 0))
pixels.show()

while True:
    checkPattern(sequence=[LEFT, RIGHT, LEFT, OUTWARD, INWARD])
    unlock()


