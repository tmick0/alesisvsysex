from alesisvsysex.protocol.types import *
from alesisvsysex.protocol.model import AlesisV
from alesisvsysex.protocol.sysex import SysexMessage

def test_sysex_serialize_query():
    q = SysexMessage('query')
    assert q.serialize() == bytes([0xf0, 0x00, 0x00, 0x0e, 0x00, 0x41, 0x62, 0x00, 0x5d, 0xf7])

def test_deserialize_query():
    b = bytes([0xf0, 0x00, 0x00, 0x0e, 0x00, 0x41, 0x62, 0x00, 0x5d, 0xf7])
    r = SysexMessage.deserialize(b)
    assert r.type == 'query'

def test_sysex_serialize_update():
    q = SysexMessage('update', AlesisV())
    begin = bytes([0xf0, 0x00, 0x00, 0x0e, 0x00, 0x41, 0x61, 0x00, 0x5d])
    end = bytes([0xf7])
    res = q.serialize()
    assert res[0:len(begin)] == begin and res[-len(end):] == end

def test_sysex_deserialize_reply():
    m = AlesisV()
    m.buttons.button1.cc = IntValue(0x55)
    
    q = SysexMessage('reply', m)
    b = q.serialize()
    
    r = SysexMessage.deserialize(b)
    assert r.type == 'reply'
    assert r.model.buttons.button1.cc.as_int() == 0x55

