RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def wheel(pos, brightness = 1):
    """
    Input a value 0 to 255 to get a color value
    :param pos:
    :return:
    """
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int((255 - pos * 3) * brightness), int(pos * 3 * brightness), 0)
    if pos < 170:
        pos -= 85
        return (0, int((255 - pos * 3) * brightness), int(pos * 3 * brightness))
    pos -= 170
    return (int(pos * 3 * brightness), 0, int((255 - pos * 3) * brightness))
