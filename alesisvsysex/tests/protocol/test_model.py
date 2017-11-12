from alesisvsysex.protocol.model import *

def test_keys_getattr():
    k = Keys(0x01, 0x02, 0x03, 0x04)
    assert k.base_note == 0x01 and k.octave == 0x02 and k.channel == 0x03 and k.curve == 0x04
    
def test_keys_bad_getattr():
    k = Keys()
    try:
        k.foo
        assert False
    except AttributeError:
        assert True
    
def test_keys_default_const():
    k = Keys()
    d = dict(k._PARAMS)
    assert k.base_note == d['base_note'] and k.octave == d['octave'] and k.channel == d['channel']

def test_keys_kwarg_const():
    k = Keys(octave=0x99)
    d = dict(k._PARAMS)
    assert k.base_note == d['base_note'] and k.octave == 0x99 and k.channel == d['channel']

def test_keys_bad_kwarg_const():
    try:
        k = Keys(foo=0x99)
        assert False
    except ValueError:
        assert True

def test_keys_setattr():
    k = Keys(0x01, 0x02, 0x03, 0x04)
    k.base_note = 0xaa
    k.octave = 0xbb
    k.channel = 0xcc
    k.curve = 0xdd
    assert k.base_note == 0xaa and k.octave == 0xbb and k.channel == 0xcc and k.curve == 0xdd

def test_keys_num_bytes():
    k = Keys()
    assert k.num_bytes() == 4

def test_keys_serialize():
    k = Keys(0x0a, 0x0b, 0x0c, 0x0d)
    assert k.serialize() == bytes([0x0a, 0x0b, 0x0c, 0x0d])

def test_keys_deserialize():
    b = bytes([0x0d, 0x0c, 0x0b, 0x0a])
    k = Keys.deserialize(b)
    assert k.base_note == 0x0d and k.octave == 0x0c and k.channel == 0x0b and k.curve == 0x0a

def test_keys_copy():
    k1 = Keys(octave=0x00)
    k2 = k1.copy()
    assert k2.octave == 0x00
    
    k1.octave = 0xaa
    assert k1.octave == 0xaa
    assert k2.octave == 0x00
    
    k2.octave = 0xbb
    assert k1.octave == 0xaa
    assert k2.octave == 0xbb

def test_knobs_default_const():
    k = Knobs()
    assert k.knob1.cc == 0x14

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
    assert k.knob1.cc == 0xaa and k.knob2.cc == 0xbb and k.knob3.cc == 0xcc and k.knob4.cc == 0xdd

def test_knobs_copy():
    k1 = Knobs()
    k1.knob1.cc = 0x10
    k2 = k1.copy()
    assert k1.knob1.cc == 0x10
    
    k1.knob1.cc = 0x11
    assert k1.knob1.cc == 0x11
    assert k2.knob1.cc == 0x10
    
    k2.knob1.cc = 0x12
    assert k1.knob1.cc == 0x11
    assert k2.knob1.cc == 0x12

def test_pads_default_const():
    p = Pads()
    assert p.pad1.note == 0x31

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
    assert (p.pad1.note == 0x01 and p.pad2.note == 0x02
            and p.pad3.note == 0x03 and p.pad4.note == 0x04
            and p.pad5.note == 0x05 and p.pad6.note == 0x06
            and p.pad7.note == 0x07 and p.pad8.note == 0x08)

def test_buttons_default_const():
    b = Buttons()
    assert b.button1.cc == 0x30

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
    assert b.button1.cc == 0x40 and b.button2.cc == 0x41 and b.button3.cc == 0x42 and b.button4.cc == 0x43

def test_alesisv_default_const():
    a = AlesisV()
    assert a.buttons.button1.cc == 0x30

