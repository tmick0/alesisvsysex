import struct

class AbstractBaseValue (object):
    pass
    
class AbstractEnumValue (AbstractBaseValue):

    _VALUES = {}

    def __init__(self, val):
        if isinstance(val, int):
            try:
                self._value = next(k for k, v in self._VALUES.items() if v == val)
            except StopIteration:
                raise ValueError("Invalid value '%d' for enum '%s'"
                                 % (val, self.__class__.__name__))
        elif isinstance(val, str):
            if val in self._VALUES:
                self._value = val
            else:
                raise ValueError("Invalid value '%s' for enum '%s'"
                                 % (val, self.__class__.__name__))
        else:
            raise ValueError("Enum must be instantiated with int or string.")
        
    def as_string(self):
        return self._value
    
    def as_int(self):
        return self._VALUES[self._value]
    
    def enum_vals(self):
        return self._VALUES.items()
        
    def serialize(self):
        return struct.pack('B', self.as_int())
    
    @classmethod
    def num_bytes(cls):
        return 1
    
    @classmethod
    def deserialize(cls, b):
        return cls(int(b[0]))
    
class IntValue (AbstractBaseValue):

    def __init__(self, val):
        if not isinstance(val, int):
            raise ValueError("Invalid type '%s', expected int."
                             % (val.__class__.__name__))
        self._value = val

    def as_int(self):
        return self._value
        
    def serialize(self):
        return struct.pack('B', self.as_int())
        
    @classmethod
    def num_bytes(cls):
        return 1
    
    @classmethod
    def deserialize(cls, b):
        return cls(int(b[0]))

class KnobModeEnum (AbstractEnumValue):

    _VALUES = {
        'CC':           0x00,
        'Aftertouch':   0x01
    }
    
class PadModeEnum (AbstractEnumValue):
    
    _VALUES = {
        'Note':         0x00,
        'Toggle CC':    0x01,
        'Momentary CC': 0x02
    }
    
class ButtonModeEnum (AbstractEnumValue):

    _VALUES = {
        'Toggle CC':    0x00,
        'Momentary CC': 0x01
    }

