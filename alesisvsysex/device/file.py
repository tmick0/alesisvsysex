from alesisvsysex.protocol.model import AlesisV, AlesisVMini

__all__ = ['FileDevice']

_MODELS = [AlesisV, AlesisVMini]

class FileDevice (object):
    
    def __init__(self, filename):
        self.filename = filename

    def get_config(self):
        with open(self.filename, 'rb') as f:
            b = f.read()
        for model in _MODELS:
            if len(b) == model.num_bytes():
                return model.deserialize(b)
        raise ValueError("'%s' is %d bytes, which matches no known device (%s)"
                         % (self.filename, len(b),
                            ', '.join('%s: %d' % (m.__name__, m.num_bytes()) for m in _MODELS)))
    
    def set_config(self, model):
        with open(self.filename, 'wb') as f:
            f.write(model.serialize())

