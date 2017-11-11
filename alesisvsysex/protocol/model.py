import struct

__all__ = ['AlesisV', 'Keys' , 'PitchWheel', 'ModWheel', 'Sustain', 'Knob', 'Knobs', 'Pad', 'Pads', 'Button', 'Buttons']

class AlesisV (object):

    def __init__(self):
        self.keys = Keys()
        self.pwheel = PitchWheel()
        self.mwheel = ModWheel()
        self.sustain = Sustain()
        self.knobs = Knobs()
        self.pads = Pads()
        self.buttons = Buttons()
    
class BasicComponent (object):
    
    _PARAMS = []
    
    def __init__(self, *args, **kwargs):
    
        # Initialize with default arguments
        self._params = {k: v for k, v in self._PARAMS}
        
        # Try to initialize from positional arguments, if any
        if len(args):
            if len(args) == len(self._PARAMS):
                for (v, (k, _)) in zip(args, self._PARAMS):
                    self._params[k] = v
            else:
                raise ValueError("Invalid argument count for component '%s': "
                                 "Expected %d, got %d."
                                 % (self.__class__.__name__, len(self._PARAMS),
                                    len(args)))
        
        # Override with keyword arguments
        for k, v in kwargs.items():
            try:
                next(kk for kk, _ in self._PARAMS if kk == k)
                self._params[k] = v
            except StopIteration:
                raise ValueError("Invalid argument '%s' for component '%s'."
                                 % (k, self.__class__.__name__))
    
    def serialize(self):
        return struct.pack("B" * len(self._PARAMS),
                           *[self._params[k] for (k, _) in self._PARAMS])
    
    def __setattr__(self, attr, value):
        if '_params' in self.__dict__ and attr in self._params:
            self._params[attr] = value
        else:
            return super().__setattr__(attr, value)
    
    def __getattr__(self, attr):
        try:
            return self.__dict__['_params'][attr]
        except KeyError:
            raise AttributeError
    
    @classmethod
    def num_bytes(cls):
        return len(cls._PARAMS)
    
    @classmethod
    def deserialize(cls, bytes):
        args = struct.unpack("B" * len(cls._PARAMS), bytes)
        return cls(*args)
    
class Keys (BasicComponent):

    _PARAMS = [
        ('base_note',   0x0c),
        ('octave',      0x02),
        ('channel',     0x00)
    ]

class PitchWheel (BasicComponent):

    _PARAMS = [
        ('channel',     0x00)
    ]

class ModWheel (BasicComponent):

    _PARAMS = [
        ('channel',     0x00),
        ('cc',          0x01),
        ('min',         0x00),
        ('max',         0x7f)
    ]
    
class Sustain (BasicComponent):

    _PARAMS = [
        ('cc',          0x40),
        ('min',         0x00),
        ('max',         0x7f),
        ('channel',     0x00)
    ]

class Knob (BasicComponent):

    _PARAMS = [
        ('mode',        0x00),
        ('cc',          0xff), # intentionally invalid
        ('min',         0x00),
        ('max',         0x7f),
        ('channel',     0x00)
    ]
    
class Knobs (object):

    def __init__(self, *args, **kwargs):
        self.knob1 = Knob(cc=0x14)
        self.knob2 = Knob(cc=0x15)
        self.knob3 = Knob(cc=0x16)
        self.knob4 = Knob(cc=0x17)
        
        if len(args):
            if len(args) == 4 and all(isinstance(k, Knob) for k in args):
                self.knob1, self.knob2, self.knob3, self.knob4 = args
            else:
                raise ValueError("To instantiate 'Knobs' component with positional "
                                 "arguments, there must be exactly 4 arguments all "
                                 "of type 'Knob'.")
        
        for k, v in kwargs.items():
            if not k in ['knob1', 'knob2', 'knob3', 'knob4']:
                raise ValueError("Invalid attribute '%s' for 'Knobs'." % k)
            if not isinstance(v, Knob):
                raise ValueError("Attribute '%s' must be of type 'Knob'." % k)
            setattr(self, k, v)
        
    def serialize(self):
        return (self.knob1.serialize() + self.knob2.serialize()
                + self.knob3.serialize() + self.knob4.serialize())
   
    @classmethod
    def deserialize(cls, bytes):
        l = Knob.num_bytes()
        return cls(*[Knob.deserialize(bytes[i * l : (i + 1) * l]) for i in range(4)])
    
    @classmethod
    def num_bytes(cls):
        return 4 * Knob.num_bytes()

class Pad (BasicComponent):

    _PARAMS = [
        ('mode',    0x00),
        ('note',    0xff), # intentionally invalid
        ('fixed',   0x00),
        ('curve',   0x00),
        ('channel', 0x09)
    ]

class Pads (object):

    def __init__(self, *args, **kwargs):
        self.pad1 = Pad(note=0x31)
        self.pad2 = Pad(note=0x20)
        self.pad3 = Pad(note=0x2a)
        self.pad4 = Pad(note=0x2e)
        self.pad5 = Pad(note=0x24)
        self.pad6 = Pad(note=0x25)
        self.pad7 = Pad(note=0x26)
        self.pad8 = Pad(note=0x27)
        
        if len(args):
            if len(args) == 8 and all(isinstance(k, Pad) for k in args):
                self.pad1, self.pad2, self.pad3, self.pad4, \
                    self.pad5, self.pad6, self.pad7, self.pad8 = args 
            else:
                raise ValueError("To instantiate 'Pads' component with positional "
                                 "arguments, there must be exactly 8 arguments all "
                                 "of type 'Pad'.")
        
        for k, v in kwargs.items():
            if not k in ['pad1', 'pad2', 'pad3', 'pad4', 'pad5', 'pad6', 'pad7', 'pad8']:
                raise ValueError("Invalid attribute '%s' for 'Pads'." % k)
            if not isinstance(v, Pad):
                raise ValueError("Attribute '%s' must be of type 'Pad'." % k)
            setattr(self, k, v)
        
    def serialize(self):
        return (self.pad1.serialize() + self.pad2.serialize()
                + self.pad3.serialize() + self.pad4.serialize()
                + self.pad5.serialize() + self.pad6.serialize()
                + self.pad7.serialize() + self.pad8.serialize())
   
    @classmethod
    def deserialize(cls, bytes):
        l = Pad.num_bytes()
        return cls(*[Pad.deserialize(bytes[i * l : (i + 1) * l]) for i in range(8)])
    
    @classmethod
    def num_bytes(cls):
        return 8 * Pad.num_bytes()

class Button (BasicComponent):

    _PARAMS = [
        ('mode',    0x00),
        ('cc',      0xff), # intentionally invalid
        ('on',      0x7f),
        ('off',     0x00),
        ('channel', 0x00)
    ]

class Buttons (object):

    def __init__(self, *args, **kwargs):
        self.button1 = Button(cc=0x30)
        self.button2 = Button(cc=0x31)
        self.button3 = Button(cc=0x32)
        self.button4 = Button(cc=0x33)
        
        if len(args):
            if len(args) == 4 and all(isinstance(k, Button) for k in args):
                self.button1, self.button2, self.button3, self.button4 = args
            else:
                raise ValueError("To instantiate 'Buttons' component with positional "
                                 "arguments, there must be exactly 4 arguments all "
                                 "of type 'Button'.")
        
        for k, v in kwargs.items():
            if not k in ['button1', 'button2', 'button3', 'button4']:
                raise ValueError("Invalid attribute '%s' for 'Buttons'." % k)
            if not isinstance(v, Button):
                raise ValueError("Attribute '%s' must be of type 'Button'." % k)
            setattr(self, k, v)
        
    def serialize(self):
        return (self.button1.serialize() + self.button2.serialize()
                + self.button3.serialize() + self.button4.serialize())
   
    @classmethod
    def deserialize(cls, bytes):
        l = Button.num_bytes()
        return cls(*[Button.deserialize(bytes[i * l : (i + 1) * l]) for i in range(4)])
    
    @classmethod
    def num_bytes(cls):
        return 4 * Button.num_bytes()

