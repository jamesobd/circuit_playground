"""
@Author Scott Jensen & James Jensen
@Copyright: MIT

MIC sensor utilities
NOTE: Be sure to call set_mic before using any of the mic utils
"""

### Import statements
import math
import board
import array
import audiobusio

### General setup

def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    """Remove DC bias before computing RMS"""
    minbuf = int(mean(values))
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf) for sample in values)

    return math.sqrt(samples_sum / len(values))


class SuperMic:
    """A class to give the mic super powers!"""

    mic = None
    samples = array.array('H', [0] * 160)
    min_magnitude = 0
    max_magnitude = 1000

    def __init__(self, sample_rate=16000, bit_depth=16):
        self.mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=sample_rate, bit_depth=bit_depth)

        # Record an initial sample to calibrate. Assume it's quiet when we start.
        self.mic.record(self.samples, len(self.samples))
        # Set lowest level to expect, plus a little.
        self.min_magnitude = normalized_rms(self.samples) + 10

        # Corresponds to sensitivity: lower means more pixels light up with lower sound
        # Adjust this as you see fit.
        self.max_magnitude = self.min_magnitude + 500

    def set_mic(mic):
        self.mic = mic

    def get_mic(self):
        return self.mic

    def get_mic_magnitude(self):
        self.mic.record(self.samples, len(self.samples))
        return normalized_rms(self.samples)

    def set_magnitude_range(self, min_magnitude=None, max_magnitude=None):
        if min_magnitude is not None:
            self.min_magnitude = min_magnitude
        else:
            self.min_magnitude = self.get_mic_magnitude() + 10

        if max_magnitude is not None:
            self.max_magnitude = max_magnitude
        else:
            self.max_magnitude = self.min_magnitude + 500

