from PyQt5.QtWidgets import *
from alesisvsysex.protocol.types import AbstractEnumValue, IntValue
from alesisvsysex.protocol.model import AlesisV, CompoundComponent, BasicComponent

__all__ = ['AlesisVSysexApplication']

class ActionMenuWidget (QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initLayout()
    
    def initLayout(self):
        layout = QHBoxLayout()
        
        bsavef = QPushButton('Save To File', self)
        layout.addWidget(bsavef)
        
        bloadf = QPushButton('Load From File', self)
        layout.addWidget(bloadf)
        
        bsaved = QPushButton('Save To Device', self)
        layout.addWidget(bsaved)
        
        bloadd = QPushButton('Load From Device', self)
        layout.addWidget(bloadd)
        
        self.setLayout(layout)
        self.setFixedHeight(50)

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

class IntegerSelector (QSpinBox):
    def __init__(self, parent, field, model):
        super().__init__(parent)
        self.fieldName = field
        self.componentModel = model

class EnumSelector (QComboBox):
    def __init__(self, parent, field, model):
        super().__init__(parent)
        self.fieldName = field
        self.componentModel = model
        for k, v in sorted(model._params[field]._VALUES.items(), key=lambda x: x[1]):
            self.addItem(k, v)

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

class EditorWidget (QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.model = self.parentWidget().parentWidget().model
        self.initLayout()
        
    def initLayout(self):
        pane1l = QVBoxLayout()
        pane1l.addWidget(BasicWidget(self, "Keys", self.model.keys))
        pane1l.addWidget(BasicWidget(self, "Pitch Wheel", self.model.pwheel))
        pane1l.addWidget(BasicWidget(self, "Mod Wheel", self.model.mwheel))
        pane1l.addWidget(BasicWidget(self, "Sustain", self.model.sustain))
        
        pane1 = QWidget()
        pane1.setLayout(pane1l)
        
        pane2l = QVBoxLayout()
        pane2l.addWidget(CompoundWidget(self, "Knobs", self.model.knobs))
        pane2l.addWidget(CompoundWidget(self, "Buttons", self.model.buttons))
        
        pane2 = QWidget()
        pane2.setLayout(pane2l)
        
        pane3l = QVBoxLayout()
        pane3l.addWidget(CompoundWidget(self, "Pads", self.model.pads))
        
        pane3 = QWidget()
        pane3.setLayout(pane3l)
        
        layout = QHBoxLayout()
        layout.addWidget(pane1)
        layout.addWidget(pane2)
        layout.addWidget(pane3)
        
        self.setLayout(layout)

class MainWidget (QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initLayout()
    
    def initLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(ActionMenuWidget(self))
        layout.addWidget(EditorWidget(self))
        self.setLayout(layout)

class AlesisVSysexApplication (QMainWindow):

    def __init__(self):
        super().__init__()
        self.model = AlesisV()
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle('Alesis V-Series SysEx Editor')
        self.setGeometry(0, 0, 640, 480)
        self.initMenu()
        self.initWidget()
        self.statusBar().showMessage('Ready.')
        self.show()
        self.clean = True

    def initMenu(self):
        menu = self.menuBar()
        mfile = menu.addMenu('File')
        
        bexit = QAction('Exit', self)
        bexit.setShortcut('Ctrl+Q')
        bexit.setStatusTip('Exit application')
        bexit.triggered.connect(self.handleExit)
        mfile.addAction(bexit)
        
    def initWidget(self):
        self.widget = MainWidget(self)
        self.setCentralWidget(self.widget)
        
    def handleExit(self):
        if self.clean:
            self.close()
        else:
            self.promptExit()
    
    def promptExit(self):
        reply = QMessageBox.question(self, "Exit",
                                     "You have unsaved changes. Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

