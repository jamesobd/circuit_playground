# Loudness Awareness Module

import array
import audiobusio
import board
import neopixel
import time

# Number of total pixels - 10 build into Circuit Playground
def mean(values):
    return sum(values) / len(values)


def blinkForever():
    while True:
        pixels.fill(0)
        pixels.show()
        time.sleep(1)
        pixels.fill((255,0,0))
        pixels.show()
        time.sleep(.2)


# Main program
# Input variables
threshold = 34300  # Setting a threshold for loudness
numSamples = 20  # Number of audio recordings for averaging data
numEventsAllowed = 5 # The number of loud events that can be recorded before blinking forever

# Set up NeoPixels and turn them all off.
NUM_PIXELS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.8, auto_write=False)
pixels.fill(0)
pixels.show()

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
                       sample_rate=16000, bit_depth=16)

# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * numSamples)
mic.record(samples, len(samples))
# Set lowest level to expect, plus a little.

numLoudEvents = 0
peak = 0
while True:
    time.sleep(0.1)
    mic.record(samples, len(samples))
    meanVal = mean(samples)
    if meanVal > threshold:
        pixels[numLoudEvents]=(255, 0, 0)
        pixels.show()
        numLoudEvents += 1
        if numLoudEvents == numEventsAllowed:
            blinkForever()
        time.sleep(4)
