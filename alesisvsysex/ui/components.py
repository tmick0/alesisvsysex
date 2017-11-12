from PyQt5.QtWidgets import *
from alesisvsysex.protocol.types import AbstractEnumValue, IntValue
from alesisvsysex.protocol.model import AlesisV, CompoundComponent, BasicComponent
from alesisvsysex.ui.values import *

class BasicWidget (QGroupBox):
    
    def __init__(self, parent, name, model):
        super().__init__(name, parent)
        self.componentName = name
        self.componentModel = model
        self.initLayout()
    
    def initLayout(self):
        layout = QFormLayout()
        
        for field, cls, _ in self.componentModel._PARAMS:
            fieldName = QLabel(field)
            if issubclass(cls, IntValue):
                fieldValue = IntegerSelector(self, field, self.componentModel)
            elif issubclass(cls, AbstractEnumValue):
                fieldValue = EnumSelector(self, field, self.componentModel)
            layout.addRow(fieldName, fieldValue)
        
        self.setLayout(layout)

class CompoundWidget (QGroupBox):
    
    def __init__(self, parent, name, model):
        if name is not None:
            super().__init__(name, parent)
        else:
            super().__init__(parent)
        self.componentName = name
        self.componentModel = model
        self.initLayout()
    
    def initLayout(self):
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        for name, _, __ in self.componentModel._COMPONENTS:
            model = self.componentModel._components[name]
            if isinstance(model, BasicComponent):
                layout.addWidget(BasicWidget(self, name, model))
            elif isinstance(model, CompoundComponent):
                layout.addWidget(CompoundWidget(self, name, model))
        self.setLayout(layout)

