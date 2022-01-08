"""
Code written to change colors of lights when the sequence that is played over the speaker repeated

by Scott Jensen
"""

import time
import board
import neopixel
import mic_utils
import simpleio
import random
from adafruit_circuitplayground.express import cpx


def start_note(freq):
    cpx.start_tone(freq)

def stop_note():
    cpx.stop_tone()

def get_freq(interval):
    return([tones[i] for i in range(len(wait_times)) if wait_times[i]==interval][0])

def play_code_note(interval):
    start_note(get_freq(interval))

def play_timed_note(freq,length):
    start_note(freq)
    time.sleep(length)
    stop_note()

def change_color(pixs, color):
    for pix in pixs:
        pixels[pix] = color
    pixels.show()

def setup_lights(lights='cp', pixNum=10):
    if lights == 'A1':
        pixels = neopixel.NeoPixel(board.A1, pixNum, brightness=.5, auto_write=False)
    elif lights == 'cp':
        pixels = cpx.pixels
    return(pixels)

def blink_pix(pixs,blink_time,blink_color):
    curr_color = pixels[0]
    change_color(pixs,blink_color)
    time.sleep(blink_time)
    change_color(pixs,curr_color)

def blink_code(code,pixs,blink_time,blink_color):
    for delay in code:
        play_code_note(delay)
        blink_pix(pixs, blink_time, blink_color)
        stop_note()
        time.sleep(delay-blink_time) #Compensate for time light is on
    play_code_note(code[-1])
    blink_pix(pixs, blink_time, blink_color)
    stop_note()

def blink_code_silent(code,pixs,blink_time,blink_color):
    for delay in code:
        blink_pix(pixs, blink_time, blink_color)
        time.sleep(delay-blink_time) #Compensate for time light is on
    blink_pix(pixs, blink_time, blink_color)

def give_code(code,pixs,blink_time,blink_color):
    print (cpx.switch)
    if cpx.switch ==False:
        blink_code(code,pixs,blink_time,blink_color)
    else:
        blink_code_silent(code,pixs,blink_time,blink_color)

def generate_code(len_range, wait_times = [0.25,0.5,1]):
    code_len = random.randint(min(len_range),max(len_range))
    code = [random.choice(wait_times) for i in range(code_len)]
    return(code)

def heard_signal(threshold):
    return(simpleio.map_range(mic.get_mic_magnitude(), 15, 1000, 0, 1)>threshold)

def update_sequence(seq,interval):
    seq[0:-1]=seq[1:]
    seq[-1] = interval
    return (seq)

def norm_sequence(code,sequence):
    return([s*sum(code)/sum(sequence) for s in sequence])

def validate_code(code,sequence):
    """
    Checks sequence to see if it matches the code
    """
    norm_s = norm_sequence(code,sequence)
    diff = [abs(code[i]-norm_s[i]) for i in range(len(code))]
    print(code,norm_s)
    if (max(diff)<allowed_timing_error) and sum(diff)<total_perc_error/100.*sum(code):
        return(True)
    return(False)

def check_code(code,listen_time,):
    start_time = time.time()
    seq = [0.]*len(code)
    current_signal=time.monotonic()
    while (time.time()-start_time)<12 and time.time()>=start_time:
        if heard_signal(threshold) == True:
            prev_signal = current_signal
            current_signal = time.monotonic()
            sequence=update_sequence(seq,current_signal-prev_signal)
            if validate_code(code,sequence) == True:
                return(True)
            while heard_signal(threshold) == True:
                pass
            time.sleep(0.05) #Set a delay to not record the same sound
    return(False)

def play_sequence(notes, lengths, rests):
    for i in range(len(notes)):
        if notes[i] != None:
            play_timed_note(notes[i],lengths[i])
            time.sleep(rests[i])
        if notes[i]==None:
            time.sleep(lengths[i])


def play_victory():
    notes = [G4,C5,E5,G5,E5,G5]
    lengths = [0.15,0.15,0.15,0.15,0.075,0.6]
    rests = [0,0,0,0.075,0,0]
    play_sequence(notes, lengths, rests)

def blink_pix(pixs,blink_time,blink_color):
    curr_color = pixels[0]
    change_color(pixs,blink_color)
    time.sleep(blink_time)
    change_color(pixs,curr_color)

def all_blink(pixs,light_intervals,blink_colors,intensity):
    blink_colors_new = intensity_color_converter(blink_colors, intensity)
    for i in range(len(light_intervals)):
        change_color(pixs,blink_colors_new[i])
        time.sleep(light_intervals[i])

def intensity_color_converter(colors, intensity):
    newColors=[]
    for color in colors:
        newColors.append(tuple(int(c*intensity) for c in color))
    return(newColors)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255,33,0)
OFF = (0, 0, 0)
colors = [RED,ORANGE]
#Notes
G4=391.995
G5=783.99
C5=523.25
E5=659.26

#Error Setup
allowed_timing_error,total_perc_error = 0.15,10

#Code Setup
num_interval_range = [2,1,1,]
relative_times = [2,1,1,1,4,1,2,1,1,1,1,3,1,1,3,1]
absolute_times = [i*0.4 for i in relative_times]
blink_colors_r = [RED,OFF]*8
blink_colors_o = [ORANGE,OFF]*8

# Mic setup
mic = mic_utils.SuperMic()
threshold = 0.15 #value from 0 to 1

#Pixel Setup
#pixCount = 10

#pixels = setup_lights() #cp for circuit python, pin otherwise

pixCount = 50
pixels = setup_lights(lights = 'A1', pixNum=pixCount) #cp for circuit python, pin otherwise
pixels.brightness = 0.8
allPixs = range(pixCount)
while True:

    all_blink(allPixs, absolute_times, blink_colors_r,0.35)
    all_blink(allPixs, absolute_times, blink_colors_o,0.35)
    all_blink(allPixs, absolute_times, blink_colors_r,0.15)
    all_blink(allPixs, absolute_times, blink_colors_o,0.15)
