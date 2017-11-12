import struct

__all__ = ['CompoundComponent', 'BasicComponent']

class CompoundComponent (object):
    
    _COMPONENTS = []
    
    def __init__(self, *args, **kwargs):
    
        # Initialize with default arguments
        self._components = {k: cls(**v) for k, cls, v in self._COMPONENTS}
        
        # Try to initialize from positional arguments, if any
        if len(args):
            if len(args) == len(self._COMPONENTS):
                for (v, (k, cls, _)) in zip(args, self._COMPONENTS):
                    if not isinstance(v, cls):
                        raise ValueError("Got type '%s' for component '%s', "
                                         "expected a '%s'."
                                         % (v.__class__.__name__, k,
                                            cls.__name__))
                    self._components[k] = v
            else:
                raise ValueError("Invalid argument count for component '%s': "
                                 "Expected %d, got %d."
                                 % (self.__class__.__name__, len(self._COMPONENTS),
                                    len(args)))
        
        # Override with keyword arguments
        for k, v in kwargs.items():
            try:
                cls = next(cls for kk, cls, _ in self._COMPONENTS if kk == k)
                if not isinstance(v, cls):
                    raise ValueError("Got type '%s' for component '%s', "
                                     "expected a '%s'."
                                     % (v.__class__.__name__, k,
                                        cls.__name__))
                self._components[k] = v
            except StopIteration:
                raise ValueError("Invalid argument '%s' for component '%s'."
                                 % (k, self.__class__.__name__))
     
    def copy(self):
        return self.__class__(**{k: v.copy() for k, v in self._components.items()})
     
    def serialize(self):
        return b''.join(self._components[k].serialize() for k, cls, _ in self._COMPONENTS)
        
    def __setattr__(self, attr, value):
        if '_components' in self.__dict__ and attr in self._params:
            self._components[attr] = value
        else:
            return super().__setattr__(attr, value)
    
    def __getattr__(self, attr):
        try:
            return self.__dict__['_components'][attr]
        except KeyError:
            raise AttributeError
    
    @classmethod
    def num_bytes(cls):
        return sum(c.num_bytes() for k, c, _ in cls._COMPONENTS)
    
    @classmethod
    def deserialize(cls, bytes):
        idx = 0
        args = []
        for k, comp, _ in cls._COMPONENTS:
            l = comp.num_bytes()
            args.append(comp.deserialize(bytes[idx:idx+l]))
            idx += l
        return cls(*args)
    
class BasicComponent (object):
    
    _PARAMS = []
    
    def __init__(self, *args, **kwargs):
    
        # Initialize with default arguments
        self._params = {k: cls(*args) for k, cls, args in self._PARAMS}
        
        # Try to initialize from positional arguments, if any
        if len(args):
            if len(args) == len(self._PARAMS):
                for (v, (k, cls, _)) in zip(args, self._PARAMS):
                    self._params[k] = v
            else:
                raise ValueError("Invalid argument count for component '%s': "
                                 "Expected %d, got %d."
                                 % (self.__class__.__name__, len(self._PARAMS),
                                    len(args)))
        
        # Override with keyword arguments
        for k, v in kwargs.items():
            try:
                cls = next(cls for kk, cls, _ in self._PARAMS if kk == k)
                if not isinstance(v, cls):
                    raise ValueError("Invalid type '%s' for field '%s' - expected '%s'."
                                     % (v.__class__.__name__, k, cls.__name__))
                self._params[k] = v
            except StopIteration:
                raise ValueError("Invalid argument '%s' for component '%s'."
                                 % (k, self.__class__.__name__))
    
    def copy(self):
        return self.__class__(**{k: v for k, v in self._params.items()})
    
    def serialize(self):
        return b''.join([self._params[k].serialize() for (k, cls, _) in self._PARAMS])
    
    def __setattr__(self, attr, value):
        if '_params' in self.__dict__ and attr in self._params:
            self._params[attr] = value
        else:
            return super().__setattr__(attr, value)
    
    def __getattr__(self, attr):
        try:
            return self.__dict__['_params'][attr]
        except KeyError:
            raise AttributeError
    
    @classmethod
    def num_bytes(cls):
        return sum(cls2.num_bytes() for k, cls2, _ in cls._PARAMS)
    
    @classmethod
    def deserialize(cls, bytes):
        idx = 0
        args = []
        for k, cls2, _ in cls._PARAMS:
            l = cls2.num_bytes()
            args.append(cls2.deserialize(bytes[idx:idx+l]))
            idx += l
        return cls(*args)

