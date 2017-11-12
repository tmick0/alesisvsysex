import struct

__all__ = ['AlesisV', 'Keys' , 'PitchWheel', 'ModWheel', 'Sustain', 'Knob', 'Knobs', 'Pad', 'Pads', 'Button', 'Buttons']
    
class CompoundComponent (object):
    
    _COMPONENTS = []
    
    def __init__(self, *args, **kwargs):
    
        # Initialize with default arguments
        self._components = {k: cls(**v) for k, cls, v in self._COMPONENTS}
        
        # Try to initialize from positional arguments, if any
        if len(args):
            if len(args) == len(self._COMPONENTS):
                for (v, (k, cls, _)) in zip(args, self._COMPONENTS):
                    if not isinstance(v, cls):
                        raise ValueError("Got type '%s' for component '%s', "
                                         "expected a '%s'."
                                         % (v.__class__.__name__, k,
                                            cls.__name__))
                    self._components[k] = v
            else:
                raise ValueError("Invalid argument count for component '%s': "
                                 "Expected %d, got %d."
                                 % (self.__class__.__name__, len(self._COMPONENTS),
                                    len(args)))
        
        # Override with keyword arguments
        for k, v in kwargs.items():
            try:
                next(kk for kk, cls, _ in self._COMPONENTS if kk == k)
                if not isinstance(v, cls):
                    raise ValueError("Got type '%s' for component '%s', "
                                     "expected a '%s'."
                                     % (v.__class__.__name__, k,
                                        cls.__name__))
                self._components[k] = v
            except StopIteration:
                raise ValueError("Invalid argument '%s' for component '%s'."
                                 % (k, self.__class__.__name__))
     
    def serialize(self):
        return b''.join(self._components[k].serialize() for k, cls, _ in self._COMPONENTS)
        
    def __setattr__(self, attr, value):
        if '_components' in self.__dict__ and attr in self._params:
            self._components[attr] = value
        else:
            return super().__setattr__(attr, value)
    
    def __getattr__(self, attr):
        try:
            return self.__dict__['_components'][attr]
        except KeyError:
            raise AttributeError
    
    @classmethod
    def num_bytes(cls):
        return sum(c.num_bytes() for k, c, _ in cls._COMPONENTS)
    
    @classmethod
    def deserialize(cls, bytes):
        idx = 0
        args = []
        for k, comp, _ in cls._COMPONENTS:
            l = comp.num_bytes()
            args.append(comp.deserialize(bytes[idx:idx+l]))
            idx += l
        return cls(*args)
    
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
        ('channel',     0x00),
        ('curve',       0x00)
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
    
class Knobs (CompoundComponent):

    _COMPONENTS = [
        ('knob1', Knob, {'cc': 0x14}),
        ('knob2', Knob, {'cc': 0x15}),
        ('knob3', Knob, {'cc': 0x16}),
        ('knob4', Knob, {'cc': 0x17})
    ]

class Pad (BasicComponent):

    _PARAMS = [
        ('mode',    0x00),
        ('note',    0xff), # intentionally invalid
        ('fixed',   0x00),
        ('curve',   0x00),
        ('channel', 0x09)
    ]

class Pads (CompoundComponent):

    _COMPONENTS = [
        ('pad1', Pad, {'note': 0x31}),
        ('pad2', Pad, {'note': 0x20}),
        ('pad3', Pad, {'note': 0x2a}),
        ('pad4', Pad, {'note': 0x2e}),
        ('pad5', Pad, {'note': 0x24}),
        ('pad6', Pad, {'note': 0x25}),
        ('pad7', Pad, {'note': 0x26}),
        ('pad8', Pad, {'note': 0x27})
    ]

class Button (BasicComponent):

    _PARAMS = [
        ('mode',    0x00),
        ('cc',      0xff), # intentionally invalid
        ('on',      0x7f),
        ('off',     0x00),
        ('channel', 0x00)
    ]

class Buttons (CompoundComponent):

    _COMPONENTS = [
        ('button1', Button, {'cc': 0x30}),
        ('button2', Button, {'cc': 0x31}),
        ('button3', Button, {'cc': 0x32}),
        ('button4', Button, {'cc': 0x33})
    ]

class AlesisV (CompoundComponent):

    _COMPONENTS = [
        ('keys', Keys, {}),
        ('pwheel', PitchWheel, {}),
        ('mwheel', ModWheel, {}),
        ('sustain', Sustain, {}),
        ('knobs', Knobs, {}),
        ('pads', Pads, {}),
        ('buttons', Buttons, {})
    ]

