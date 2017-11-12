from PyQt5.QtWidgets import *
from alesisvsysex.protocol.types import *

class IntegerSelector (QSpinBox):

    def __init__(self, parent, field):
        super().__init__(parent)
        self.fieldName = field
        self.setRange(0x00, 0x7f)
        self.setSingleStep(1)
        self.updateState()
        self.valueChanged.connect(self.updateModel)
        
    def updateState(self):
        self.setValue(getattr(self.getModel(), self.fieldName).as_int())
    
    def updateModel(self):
        setattr(self.getModel(), self.fieldName, IntValue(self.value()))
    
    def getModel(self):
        return self.parent().getModel()

class EnumSelector (QComboBox):

    def __init__(self, parent, field):
        super().__init__(parent)
        self.fieldName = field
        self.enumClass = self.getModel()._params[field].__class__
        self.enumValues = list(sorted(self.enumClass._VALUES.items(), key=lambda x: x[1]))
        for k, v in self.enumValues:
            self.addItem(k, v)
        self.updateState()
        self.currentIndexChanged.connect(self.updateModel)
        
    def updateState(self):
        for i, (k, v) in enumerate(self.enumValues):
            if getattr(self.getModel(), self.fieldName).as_int() == v:
                self.setCurrentIndex(i)
                break
        else:
            raise RuntimeError("Invalid state for component '%s' field '%s'"
                               % (self.getModel().__class__.__name__, self.fieldName))
                               
    def updateModel(self):
        setattr(self.getModel(), self.fieldName, self.enumClass(self.enumValues[self.currentIndex()][1]))

    def getModel(self):
        return self.parent().getModel()

