# Import statements
import gc
import sys
import time
import board
import touchio
import digitalio
import simpleio
import analogio
import neopixel
import microcontroller
import adafruit_thermistor
import data_utils as data
import cron_utils as cron
import neopixel_utils
import mic_utils
import photosensor_utils


# Functions
def get_brightness():
    """
    Returns the light intensity detected by the photo sensor converted from a scale of (0, 20000) to (0, 1)
    Turns off the pixels to remove light pollution, waits one delay interval, and then takes a reading
    TODO: See if we can save the pixel values before clearing them so we can set them back after the reading is taken

    :return: The light intensity detected by the photo sensor converted from a scale of (0, 20000) to (0, 1)
    """
    global pixels
    pixels.fill(0)
    pixels.show()
    time.sleep(delay)
    return simpleio.map_range(light.value, 0, 20000, .1, 1)


# Variables
start_time = time.monotonic()
max_ram = 256000
delay = 0.01  # Main loop delay
display_mode = 0
button_a_pressed = False
button_b_pressed = False
brightnessObj1 = data.SuperInt(1).value
brightnessObj2 = data.SuperInt(2).value
file_write_status = None  # State of file system (None, 'rw', 'error', 'out_of_space')

# LED setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1, auto_write=False)

# Button setup
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

# Switch setup
switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Photo sensor setup
light = analogio.AnalogIn(board.LIGHT)
brightness = get_brightness()
init_brightness = brightness
# brightness = 1 # override

# Temperature setup
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)

# Touch setup
touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)

# Mic setup
mic = mic_utils.SuperMic()

# Speaker setup
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = False


# CRON jobs
# def one_second_jobs():
#     # cron.remove(0)
# cron.add(one_second_jobs, 1)

# def ten_second_jobs():
#     global brightness
#     # brightness = get_brightness()
#
#
# cron.add(ten_second_jobs, 10)

def one_minute_jobs():
    global file_write_status
    try:
        with open("/runtime.log", "a") as fp:
            now_time = time.monotonic()
            diff_time = now_time - start_time
            fp.write('{0:f}\n'.format(diff_time))
            fp.flush()
            file_write_status = 'rw'
    except OSError as e:
        if e.args[0] == 28:
            file_write_status = 'out_of_space'
        else:
            file_write_status = 'error'


cron.add(one_minute_jobs, 60)
one_minute_jobs()

# The main loop
while True:
    # Speaker control
    speaker_enable.value = switch.value

    # Sensor value aliases
    cpu_temp = microcontroller.cpu.temperature
    therm_temp = thermistor.temperature

    # Set the file system color based on file system status
    file_write_status_color = tuple(
        int(l * r) for l, r in zip(neopixel_utils.RED, (brightness, brightness, brightness)))
    if file_write_status == 'out_of_space':
        file_write_status_color = tuple(
            int(l * r) for l, r in zip(neopixel_utils.YELLOW, (brightness, brightness, brightness)))
    elif file_write_status == 'rw':
        file_write_status_color = tuple(
            int(l * r) for l, r in zip(neopixel_utils.GREEN, (brightness, brightness, brightness)))

    # Calculate color to display for temperatures
    cpu_temp_color_red = int(
        simpleio.map_range(cpu_temp, 20, 40, 0, 255))  # Scale the value of temp from (20, 40) to (0, 255)
    cpu_temp_color_blue = 255 - cpu_temp_color_red
    therm_temp_color_red = int(
        simpleio.map_range(therm_temp, 15, 40, 0, 255))  # Scale the value of temp from (15, 40) to (0, 255)
    therm_temp_color_blue = 255 - therm_temp_color_red
    # adjust color brightness based on ambient brightness
    cpu_temp_color_red = int(cpu_temp_color_red * brightness)
    cpu_temp_color_blue = int(cpu_temp_color_blue * brightness)
    therm_temp_color_red = int(therm_temp_color_red * brightness)
    therm_temp_color_blue = int(therm_temp_color_blue * brightness)

    if touch_A1.value:
        print("A1 touched!")
    if touch_A2.value:
        print("A2 touched!")
    if touch_A3.value:
        print("A3 touched!")
    if touch_A4.value:
        print("A4 touched!")
    if touch_A5.value:
        print("A5 touched!")
    if touch_A6.value:
        print("A6 touched!")
    if touch_TX.value:
        print("TX touched!")

    # Detect a leading buttondown on button A with a debounce until buttonup
    # TODO: Move this to a button utils library.  Add leading and trailing button options and maybe a time 'wait' option
    if button_a.value and not button_a_pressed:
        button_a_pressed = button_a.value
        # Change display_mode
        display_mode = (display_mode + 1) % 6
    else:
        button_a_pressed = button_a.value

    if button_b.value and not button_b_pressed:
        button_b_pressed = button_b.value
        # Change brightness
        if brightness == 1:
            brightness = get_brightness()
        else:
            brightness = 1
    else:
        button_b_pressed = button_b.value

    # Change the color of the lights
    if display_mode == 0:
        pixels.fill(0)
        # Display different sensor outputs for each light
        pixels[0] = (cpu_temp_color_red, 0, cpu_temp_color_blue)  # CPU temperature
        pixels[1] = (therm_temp_color_red, 0, therm_temp_color_blue)  # Thermistor temperature
        pixels[2] = neopixel_utils.wheel(int(simpleio.map_range(mic.get_mic_magnitude(), 15, 1000, 0, 255)),
                                         brightness)  # Mic sound magnitude
        pixels[3] = (int(simpleio.map_range(max_ram - gc.mem_free(), 0, 256000, 0, 255) * brightness),
                     int(simpleio.map_range(gc.mem_free(), 0, 256000, 0, 255) * brightness), 0)
        pixels[4] = (file_write_status_color)  # File system status color
    elif display_mode == 1:
        # Display the CPU temperature
        pixels.fill((cpu_temp_color_red, 0, cpu_temp_color_blue))
    elif display_mode == 2:
        pixels.fill((therm_temp_color_red, 0, therm_temp_color_blue))
    elif display_mode == 3:
        pixels.fill(
            neopixel_utils.wheel(int(simpleio.map_range(mic.get_mic_magnitude(), 15, 1000, 0, 255)), brightness))
    elif display_mode == 4:
        pixels.fill((int(simpleio.map_range(max_ram - gc.mem_free(), 0, 256000, 0, 255) * brightness),
                     int(simpleio.map_range(gc.mem_free(), 0, 256000, 0, 255) * brightness), 0))
    elif display_mode == 5:
        pixels.fill(file_write_status_color)  # File system status color

    pixels.show()

    # time.sleep(delay)
    cron.next()
