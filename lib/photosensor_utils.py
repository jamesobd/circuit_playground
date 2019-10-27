"""
@Author Scott Jensen & James Jensen
@Copyright: MIT

Photo sensor utilities
"""

### Import statements

### General setup

def get_brightness(pixels):
    """
    Returns the light intensity detected by the photo sensor converted from a scale of (0, 20000) to (0, 1)
    Turns off the pixels to remove light pollution, waits one delay interval, and then takes a reading
    TODO: See if we can save the pixel values before clearing them so we can set them back after the reading is taken

    :return: The light intensity detected by the photo sensor converted from a scale of (0, 20000) to (0, 1)
    """
    pixels.fill(neopixel_utils.OFF)
    pixels.show()
    time.sleep(delay)
    return simpleio.map_range(light.value, 0, 20000, 0, 1)
