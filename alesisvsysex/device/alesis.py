import mido
from alesisvsysex.protocol.sysex import SysexMessage

__all__ = ['AlesisV25Device']

class AlesisV25Device (object):
    
    _PORT_PREFIX = "V25:V25 MIDI"
    
    def __init__(self):
        for port in mido.get_ioport_names():
            if port.startswith(self._PORT_PREFIX):
                self.port = mido.open_ioport(port)
                break
        else:
            raise RuntimeError("Could not find a port named '%s'" % self._PORT_PREFIX)
    
    def __del__(self):
        try:
            self.port.close()
        except:
            pass

    def send(self, message):
        if not isinstance(message, SysexMessage):
            raise ValueError("Can only send a SysexMessage")
        p = mido.Parser()
        p.feed(message.serialize())
        self.port.send(p.get_message())

    def recv(self):
        while True:
            r = self.port.receive()
            if r.type == 'sysex':
                break
        return SysexMessage.deserialize(r.bin())

