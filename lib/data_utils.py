"""
@Author Scott Jensen & James Jensen
@Copyright: MIT

Useful data tools for validation, transitions, and so on
"""

class SuperInt:
    """A reusable class to create a data value with super powers!"""

    _max = None
    _min = None

    def __init__(self, startValue):
        self._value = startValue

    def setMax(maxVal):
        self._max = maxVal

    def setMin(minVal):
        self._min = minVal

    #def setTransition(step, ):


    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def delValue(self):
        del self._value

    value = property(getValue, setValue, delValue, "I'm the 'value' property.")