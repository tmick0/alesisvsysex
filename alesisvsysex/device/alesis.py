import time

import mido
from alesisvsysex.protocol.sysex import SysexMessage

__all__ = ['AlesisDevice']

_PRODUCT_PREFIXES_AND_IDS = {
    "V25": 0x41,
    "V49": 0x42,
    "V61": 0x43,
    "VMini": 0x49,
}

def _matching_ports(names, prefix):
    matches = [n for n in names if n.startswith(prefix)]
    # Devices exposing several ports keep the editor port last, and name it
    # explicitly on some platforms.
    editor = [n for n in matches if 'EDITOR' in n.upper()]
    return editor or matches

class AlesisDevice (object):
    
    
    @staticmethod 
    def device_factory():
        # Input and output ports are not always named identically
        # (e.g. the VMini exposes 'VMini EDITOR Out' / 'VMini EDITOR In'),
        # so they are matched separately rather than via get_ioport_names().
        input_names = mido.get_input_names()
        output_names = mido.get_output_names()
        for product_prefix, product_id in _PRODUCT_PREFIXES_AND_IDS.items():
            inputs = _matching_ports(input_names, product_prefix)
            outputs = _matching_ports(output_names, product_prefix)
            if inputs and outputs:
                return AlesisDevice(inputs[-1], outputs[-1], product_id)
        # If we get here, no supported port names were found
        target_prefix_list = "','".join(_PRODUCT_PREFIXES_AND_IDS.keys())
        raise RuntimeError(
            "Could not find a MIDI input and output pair with a prefix in '%s'.\n"
            "Inputs: %s\nOutputs: %s"
            % (target_prefix_list, input_names, output_names))

    def __init__(self, input_name, output_name, product_id):
        self.input_name = input_name
        self.output_name = output_name
        self.product_id = product_id
        self._inport = mido.open_input(input_name)
        self._outport = mido.open_output(output_name)

    @property
    def ioport_name(self):
        if self.input_name == self.output_name:
            return self.input_name
        return "%s / %s" % (self.output_name, self.input_name)

    def __del__(self):
        for attr in ('_inport', '_outport'):
            try:
                getattr(self, attr).close()
            except Exception:
                pass

    def _send(self, message):
        if not isinstance(message, SysexMessage):
            raise ValueError("Can only send a SysexMessage")
        p = mido.Parser()
        p.feed(message.serialize())
        self._outport.send(p.get_message())

    def _recv(self, timeout=2.0):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            r = self._inport.poll()
            if r is None:
                time.sleep(0.005)
            elif r.type == 'sysex':
                return SysexMessage.deserialize(r.bin())
        raise RuntimeError("No response from device on '%s'" % self.ioport_name)

    def get_config(self):
        while self._inport.poll() is not None:
            pass
        self._send(SysexMessage('query', self.product_id))
        return self._recv().model

    def default_config(self):
        return SysexMessage.model_class(self.product_id)()
    
    def set_config(self, model):
        model_bin = model.serialize()
        self._send(SysexMessage('update', self.product_id, model))
        if self.get_config().serialize() != model_bin:
            raise RuntimeError('Failed to update configuration')

