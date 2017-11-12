from alesisvsysex.protocol.types import *

def test_intval_as_int():
    v = IntValue(5)
    assert v.as_int() == 5

def test_intval_serialize():
    v = IntValue(5)
    assert v.serialize() == bytes([5])

def test_intval_deseiralize():
    assert IntValue.deserialize(bytes([5])).as_int() == 5

def test_enumval_const_str():
    v = PadModeEnum('Toggle CC')
    assert v.as_int() == 0x01

def test_enumval_const_int():
    v = PadModeEnum(0x01)
    assert v.as_int() == 0x01

def test_enumval_as_str():
    v = PadModeEnum(0x01)
    assert v.as_string() == "Toggle CC"
    
def test_enumval_serialize():
    v = PadModeEnum(0x01)
    assert v.serialize() == bytes([0x01])
    
def test_enumval_deserialiez():
    assert PadModeEnum.deserialize(bytes([0x01])).as_int() == 0x01
    
