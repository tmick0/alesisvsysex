from .model import AlesisV, AlesisVMini

__all__ = ['SysexMessage']

class SysexMessage (object):
    
    _TYPES = {
        'update': [0x61],
        'query':  [0x62],
        'reply':  [0x63]
    }
    
    _MODELS = {
        0x41: AlesisV,      # V25
        0x42: AlesisV,      # V49
        0x43: AlesisV,      # V61
        0x49: AlesisVMini,  # VMini
    }
    
    # 0xff at last byte of _HEADER_START is a placeholder for the product id
    _HEADER_START = [0x00, 0x00, 0x0e, 0x00, 0xff] 
    
    _START_BYTE = [0xf0]
    _END_BYTE   = [0xf7]
    
    def __init__(self, msg_type, product_id, model=None):
        self.type       = msg_type
        self.product_id = product_id
        self.model      = model
    
    @classmethod
    def model_class(cls, product_id):
        try:
            return cls._MODELS[product_id]
        except KeyError:
            raise ValueError("Unknown product id '0x%02x'" % product_id)
    
    @classmethod
    def _header_end(cls, product_id):
        # 14 bit payload length, least significant byte last
        n = cls.model_class(product_id).num_bytes()
        return [n >> 7, n & 0x7f]
    
    def serialize(self):
        product_header_start = list(self._HEADER_START)
        product_header_start[4] = self.product_id
        header_end = self._header_end(self.product_id)
        if self.type == 'query':
            return bytes(self._START_BYTE + product_header_start + self._TYPES[self.type]
                         + header_end + self._END_BYTE)
        else:
            return bytes(self._START_BYTE + product_header_start + self._TYPES[self.type]
                         + header_end) + self.model.serialize() + bytes(self._END_BYTE)
                     
        
    @classmethod
    def deserialize(cls, b):
        i = 0
        
        start_byte = b[i : i+1]
        if start_byte != bytes(cls._START_BYTE):
            raise ValueError("Invalid start byte '0x%02x'" % start_byte[0])
        i += 1
        
        header_start = b[i : i + len(cls._HEADER_START)]
        # the last byte of the header is the product id, which varies by device
        if header_start[:4] != bytes(cls._HEADER_START[:4]):
            raise ValueError("Invalid message header")
        product_id = header_start[4]
        i += len(cls._HEADER_START)
        
        t = b[i : i + 1]
        for k, v in cls._TYPES.items():
            if t == bytes(v):
                msg_type = k
                break
        else:
            raise ValueError("Unknown message type '0x%02x'" % t[0])
        i += 1
        
        model_cls = cls.model_class(product_id)
        header_end = b[i : i + 2]
        payload_len = (header_end[0] << 7) | header_end[1]
        if payload_len != model_cls.num_bytes():
            raise ValueError("Product 0x%02x reported a %d byte payload, expected %d"
                             % (product_id, payload_len, model_cls.num_bytes()))
        i += 2
        
        if msg_type == "query":
            model = None
        else:
            model = model_cls.deserialize(b[i : i + model_cls.num_bytes()])
            i += model_cls.num_bytes()
        
        end_byte = b[i : i+1]
        if end_byte != bytes(cls._END_BYTE):
            raise ValueError("Invalid end byte '0x%02x'" % end_byte[0])
        i += 1
        
        return SysexMessage(msg_type, product_id, model)
    
    @classmethod
    def num_bytes(cls, msg_type, product_id):
        n = (len(cls._START_BYTE) + len(cls._HEADER_START) + 1 + 2
             + len(cls._END_BYTE))
        if msg_type != 'query':
            n += cls.model_class(product_id).num_bytes()
        return n
        
