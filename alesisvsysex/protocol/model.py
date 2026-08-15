import struct

from alesisvsysex.protocol.types import *
from alesisvsysex.protocol.component import *

__all__ = ['AlesisV', 'AlesisVMini', 'Keys' , 'PitchWheel', 'ModWheel', 'Sustain', 'Knob', 'Knobs', 'MiniKnobs', 'Pad', 'Pads', 'MiniPads', 'Button', 'Buttons', 'MiniUnknown']
    
class Keys (BasicComponent):

    _PARAMS = [
        ('base_note',   IntValue,   [0x0c]),
        ('octave',      IntValue,   [0x02]),
        ('channel',     IntValue,   [0x00]),
        ('curve',       IntValue,   [0x00])
    ]

class PitchWheel (BasicComponent):

    _PARAMS = [
        ('channel',     IntValue,   [0x00])
    ]

class ModWheel (BasicComponent):

    _PARAMS = [
        ('channel',     IntValue,   [0x00]),
        ('cc',          IntValue,   [0x01]),
        ('min',         IntValue,   [0x00]),
        ('max',         IntValue,   [0x7f])
    ]
    
class Sustain (BasicComponent):

    _PARAMS = [
        ('cc',          IntValue,   [0x40]),
        ('min',         IntValue,   [0x00]),
        ('max',         IntValue,   [0x7f]),
        ('channel',     IntValue,   [0x00])
    ]

class Knob (BasicComponent):

    _PARAMS = [
        ('mode',        KnobModeEnum,   [0x00]),
        ('cc',          IntValue,       [0xff]), # intentionally invalid
        ('min',         IntValue,       [0x00]),
        ('max',         IntValue,       [0x7f]),
        ('channel',     IntValue,       [0x00])
    ]
    
class Knobs (CompoundComponent):

    _COMPONENTS = [
        ('knob1', Knob, {'cc': IntValue(0x14)}),
        ('knob2', Knob, {'cc': IntValue(0x15)}),
        ('knob3', Knob, {'cc': IntValue(0x16)}),
        ('knob4', Knob, {'cc': IntValue(0x17)})
    ]

class Pad (BasicComponent):

    _PARAMS = [
        ('mode',    PadModeEnum,    [0x00]),
        ('note',    IntValue,       [0xff]), # intentionally invalid
        ('fixed',   IntValue,       [0x00]),
        ('curve',   IntValue,       [0x00]),
        ('channel', IntValue,       [0x09])
    ]

class Pads (CompoundComponent):

    _COMPONENTS = [
        ('pad1', Pad, {'note': IntValue(0x31)}),
        ('pad2', Pad, {'note': IntValue(0x20)}),
        ('pad3', Pad, {'note': IntValue(0x2a)}),
        ('pad4', Pad, {'note': IntValue(0x2e)}),
        ('pad5', Pad, {'note': IntValue(0x24)}),
        ('pad6', Pad, {'note': IntValue(0x25)}),
        ('pad7', Pad, {'note': IntValue(0x26)}),
        ('pad8', Pad, {'note': IntValue(0x27)})
    ]

class Button (BasicComponent):

    _PARAMS = [
        ('mode',    ButtonModeEnum, [0x00]),
        ('cc',      IntValue,       [0xff]), # intentionally invalid
        ('on',      IntValue,       [0x7f]),
        ('off',     IntValue,       [0x00]),
        ('channel', IntValue,       [0x00])
    ]

class Buttons (CompoundComponent):

    _COMPONENTS = [
        ('button1', Button, {'cc': IntValue(0x30)}),
        ('button2', Button, {'cc': IntValue(0x31)}),
        ('button3', Button, {'cc': IntValue(0x32)}),
        ('button4', Button, {'cc': IntValue(0x33)})
    ]

class AlesisV (CompoundComponent):

    _COMPONENTS = [
        ('keys',    Keys,       {}),
        ('pwheel',  PitchWheel, {}),
        ('mwheel',  ModWheel,   {}),
        ('sustain', Sustain,    {}),
        ('knobs',   Knobs,      {}),
        ('pads',    Pads,       {}),
        ('buttons', Buttons,    {})
    ]

class MiniKnobs (CompoundComponent):

    _COMPONENTS = [
        ('knob1', Knob, {'cc': IntValue(0x0e)}),
        ('knob2', Knob, {'cc': IntValue(0x0f)}),
        ('knob3', Knob, {'cc': IntValue(0x10)}),
        ('knob4', Knob, {'cc': IntValue(0x11)})
    ]

class MiniPads (CompoundComponent):

    _COMPONENTS = [
        ('pad1', Pad, {'note': IntValue(0x24), 'channel': IntValue(0x00)}),
        ('pad2', Pad, {'note': IntValue(0x26), 'channel': IntValue(0x00)}),
        ('pad3', Pad, {'note': IntValue(0x2a), 'channel': IntValue(0x00)}),
        ('pad4', Pad, {'note': IntValue(0x2e), 'channel': IntValue(0x00)})
    ]

class MiniUnknown (BasicComponent):

    # Undocumented region between the key and knob settings on the VMini.
    # It is read and written back verbatim so that nothing is clobbered.
    _PARAMS = [
        ('byte1',  IntValue, [0x00]),
        ('byte2',  IntValue, [0x50]),
        ('byte3',  IntValue, [0x00]),
        ('byte4',  IntValue, [0x01]),
        ('byte5',  IntValue, [0x00]),
        ('byte6',  IntValue, [0x7f]),
        ('byte7',  IntValue, [0x40]),
        ('byte8',  IntValue, [0x00]),
        ('byte9',  IntValue, [0x40]),
        ('byte10', IntValue, [0x7f]),
        ('byte11', IntValue, [0x00]),
        ('byte12', IntValue, [0x00])
    ]

class AlesisVMini (CompoundComponent):

    _COMPONENTS = [
        ('keys',    Keys,        {}),
        ('unknown', MiniUnknown, {}),
        ('knobs',   MiniKnobs,   {}),
        ('pads',    MiniPads,    {})
    ]

