from alesisvsysex.device.alesis import *
from alesisvsysex.protocol.sysex import *
from alesisvsysex.protocol.model import *

def test_v25_constructor():
    d = AlesisV25Device()

def test_v25_send_recv():
    d = AlesisV25Device()
    m = SysexMessage('query')
    d.send(m)
    r = d.recv()

