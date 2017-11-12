from alesisvsysex.protocol.model import *
from alesisvsysex.protocol.types import *

def test_keys_getattr():
    k = Keys(IntValue(0x01), IntValue(0x02), IntValue(0x03), IntValue(0x04))
    assert k.base_note.as_int() == 0x01
    assert k.octave.as_int() == 0x02
    assert k.channel.as_int() == 0x03
    assert k.curve.as_int() == 0x04
    
def test_keys_bad_getattr():
    k = Keys()
    try:
        k.foo
        assert False
    except AttributeError:
        assert True
    
def test_keys_default_const():
    k = Keys()
    d = {kk: cls(*v) for kk, cls, v in k._PARAMS}
    assert k.base_note.as_int() == d['base_note'].as_int()
    assert k.octave.as_int() == d['octave'].as_int()
    assert k.channel.as_int() == d['channel'].as_int()
    assert k.curve.as_int() == d['curve'].as_int()

def test_keys_kwarg_const():
    k = Keys(octave=IntValue(0x99))
    d = {kk: cls(*v) for kk, cls, v in k._PARAMS}
    assert k.base_note.as_int() == d['base_note'].as_int()
    assert k.octave.as_int() == 0x99
    assert k.channel.as_int() == d['channel'].as_int()

def test_keys_bad_kwarg_const():
    try:
        k = Keys(foo=IntValue(0x99))
        assert False
    except ValueError:
        assert True

def test_keys_setattr():
    k = Keys(IntValue(0x01), IntValue(0x02), IntValue(0x03), IntValue(0x04))
    k.base_note = IntValue(0xaa)
    k.octave = IntValue(0xbb)
    k.channel = IntValue(0xcc)
    k.curve = IntValue(0xdd)
    assert k.base_note.as_int() == 0xaa
    assert k.octave.as_int() == 0xbb
    assert k.channel.as_int() == 0xcc
    assert k.curve.as_int() == 0xdd

def test_keys_num_bytes():
    k = Keys()
    assert k.num_bytes() == 4

def test_keys_serialize():
    k = Keys(IntValue(0x0a), IntValue(0x0b), IntValue(0x0c), IntValue(0x0d))
    assert k.serialize() == bytes([0x0a, 0x0b, 0x0c, 0x0d])

def test_keys_deserialize():
    b = bytes([0x0d, 0x0c, 0x0b, 0x0a])
    k = Keys.deserialize(b)
    assert k.base_note.as_int() == 0x0d
    assert k.octave.as_int() == 0x0c
    assert k.channel.as_int() == 0x0b
    assert k.curve.as_int() == 0x0a

def test_keys_copy():
    k1 = Keys(octave=IntValue(0x00))
    k2 = k1.copy()
    assert k2.octave.as_int() == 0x00
    
    k1.octave = IntValue(0xaa)
    assert k1.octave.as_int() == 0xaa
    assert k2.octave.as_int() == 0x00
    
    k2.octave = IntValue(0xbb)
    assert k1.octave.as_int() == 0xaa
    assert k2.octave.as_int() == 0xbb

def test_knobs_default_const():
    k = Knobs()
    assert k.knob1.cc.as_int() == 0x14

def test_knobs_serialize():
    k = Knobs()
    assert k.serialize() == bytes([0x00, 0x14, 0x00, 0x7f, 0x00,
                                   0x00, 0x15, 0x00, 0x7f, 0x00,
                                   0x00, 0x16, 0x00, 0x7f, 0x00,
                                   0x00, 0x17, 0x00, 0x7f, 0x00])
                                   
def test_knobs_deserialize():
    b = bytes([0x00, 0xaa, 0x00, 0x7f, 0x00,
               0x00, 0xbb, 0x00, 0x7f, 0x00,
               0x00, 0xcc, 0x00, 0x7f, 0x00,
               0x00, 0xdd, 0x00, 0x7f, 0x00])
    k = Knobs.deserialize(b)
    assert k.knob1.cc.as_int() == 0xaa
    assert k.knob2.cc.as_int() == 0xbb
    assert k.knob3.cc.as_int() == 0xcc
    assert k.knob4.cc.as_int() == 0xdd

def test_knobs_copy():
    k1 = Knobs()
    k1.knob1.cc = IntValue(0x10)
    k2 = k1.copy()
    assert k1.knob1.cc.as_int() == 0x10
    
    k1.knob1.cc = IntValue(0x11)
    assert k1.knob1.cc.as_int() == 0x11
    assert k2.knob1.cc.as_int() == 0x10
    
    k2.knob1.cc = IntValue(0x12)
    assert k1.knob1.cc.as_int() == 0x11
    assert k2.knob1.cc.as_int() == 0x12

def test_pads_default_const():
    p = Pads()
    assert p.pad1.note.as_int() == 0x31

def test_pads_serialize():
    p = Pads()
    assert p.serialize() == bytes([0x00, 0x31, 0x00, 0x00, 0x09,
                                   0x00, 0x20, 0x00, 0x00, 0x09,
                                   0x00, 0x2a, 0x00, 0x00, 0x09,
                                   0x00, 0x2e, 0x00, 0x00, 0x09,
                                   0x00, 0x24, 0x00, 0x00, 0x09,
                                   0x00, 0x25, 0x00, 0x00, 0x09,
                                   0x00, 0x26, 0x00, 0x00, 0x09,
                                   0x00, 0x27, 0x00, 0x00, 0x09])
                                   
def test_pads_deserialize():
    b = bytes([0x00, 0x01, 0x00, 0x00, 0x09,
               0x00, 0x02, 0x00, 0x00, 0x09,
               0x00, 0x03, 0x00, 0x00, 0x09,
               0x00, 0x04, 0x00, 0x00, 0x09,
               0x00, 0x05, 0x00, 0x00, 0x09,
               0x00, 0x06, 0x00, 0x00, 0x09,
               0x00, 0x07, 0x00, 0x00, 0x09,
               0x00, 0x08, 0x00, 0x00, 0x09])
    p = Pads.deserialize(b)
    assert (p.pad1.note.as_int() == 0x01 and p.pad2.note.as_int() == 0x02
            and p.pad3.note.as_int() == 0x03 and p.pad4.note.as_int() == 0x04
            and p.pad5.note.as_int() == 0x05 and p.pad6.note.as_int() == 0x06
            and p.pad7.note.as_int() == 0x07 and p.pad8.note.as_int() == 0x08)

def test_buttons_default_const():
    b = Buttons()
    assert b.button1.cc.as_int() == 0x30

def test_buttons_serialize():
    b = Buttons()
    assert b.serialize() == bytes([0x00, 0x30, 0x7f, 0x00, 0x00,
                                   0x00, 0x31, 0x7f, 0x00, 0x00,
                                   0x00, 0x32, 0x7f, 0x00, 0x00,
                                   0x00, 0x33, 0x7f, 0x00, 0x00])
                                   
def test_knobs_deserialize():
    b = bytes([0x00, 0x40, 0x7f, 0x00, 0x00,
               0x00, 0x41, 0x7f, 0x00, 0x00,
               0x00, 0x42, 0x7f, 0x00, 0x00,
               0x00, 0x43, 0x7f, 0x00, 0x00])
    b = Buttons.deserialize(b)
    assert (b.button1.cc.as_int() == 0x40 and b.button2.cc.as_int() == 0x41
            and b.button3.cc.as_int() == 0x42 and b.button4.cc.as_int() == 0x43)

def test_alesisv_default_const():
    a = AlesisV()
    assert a.buttons.button1.cc.as_int() == 0x30

