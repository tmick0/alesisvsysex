from PyQt5.QtWidgets import *
from alesisvsysex.protocol.model import AlesisV
from alesisvsysex.protocol.component import CompoundComponent
from alesisvsysex.device.alesis import AlesisDevice
from alesisvsysex.device.file import FileDevice
from alesisvsysex.ui.components import *
from alesisvsysex.ui.filedialog import *

__all__ = ['AlesisVSysexApplication']

class ActionMenuWidget (QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initLayout()
    
    def initLayout(self):
        layout = QHBoxLayout()
        
        bsavef = QPushButton('Save To File', self)
        bsavef.clicked.connect(self.propagateCommand('saveFile'))
        layout.addWidget(bsavef)
        
        bloadf = QPushButton('Load From File', self)
        bloadf.clicked.connect(self.propagateCommand('loadFile'))
        layout.addWidget(bloadf)
        
        bsaved = QPushButton('Save To Device', self)
        bsaved.clicked.connect(self.propagateCommand('saveDevice'))
        layout.addWidget(bsaved)
        
        bloadd = QPushButton('Load From Device', self)
        bloadd.clicked.connect(self.propagateCommand('loadDevice'))
        layout.addWidget(bloadd)
        
        breset = QPushButton('Reset To Defaults', self)
        breset.clicked.connect(self.propagateCommand('resetDefaults'))
        layout.addWidget(breset)
        
        self.setLayout(layout)
        self.setFixedHeight(50)
    
    def propagateCommand(self, command):
        def closure():
            getattr(self.parent().parent(), command)()
        return closure

class ContainerWidget (QWidget):

    def __init__(self):
        super().__init__()
        
    def getModel(self):
        p = self.parent()
        while not isinstance(p, EditorWidget):
            p = p.parent()
        return p.getModel()

class EditorWidget (QTabWidget):

    _LABELS = {
        'keys':    'Keys',
        'pwheel':  'Pitch Wheel',
        'mwheel':  'Mod Wheel',
        'sustain': 'Sustain',
        'knobs':   'Knobs',
        'buttons': 'Buttons',
        'pads':    'Pads',
    }

    # Components absent from the loaded model (e.g. the VMini has no
    # buttons) are skipped, as are components with no entry here.
    _TABS = [
        ("Keys / Wheels / Sustain", QHBoxLayout, ['keys', 'pwheel', 'mwheel', 'sustain']),
        ("Knobs / Buttons",         QVBoxLayout, ['knobs', 'buttons']),
        ("Pads",                    QVBoxLayout, ['pads']),
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.children = []
        self.initLayout()
        
    def addChild(self, parent, widget):
        parent.addWidget(widget)
        self.children.append(widget)
        
    def initLayout(self):
        model = self.getModel()
        for title, layoutClass, keys in self._TABS:
            present = [k for k in keys if k in model._components]
            if not present:
                continue
            layout = layoutClass()
            for k in present:
                widgetClass = (CompoundWidget
                               if isinstance(model._components[k], CompoundComponent)
                               else BasicWidget)
                self.addChild(layout, widgetClass(self, self._LABELS[k], k))
            pane = ContainerWidget()
            pane.setLayout(layout)
            if len(present) != len(keys):
                title = ' / '.join(self._LABELS[k] for k in present)
            self.addTab(pane, title)

    def getModel(self):
        return self.parentWidget().parentWidget().model
        
    def updateState(self):
        for c in self.children:
            c.updateState()

class MainWidget (QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.initLayout()
    
    def initLayout(self):
        layout = QVBoxLayout()
        self.actionWidget = ActionMenuWidget(self)
        layout.addWidget(self.actionWidget)
        self.editorWidget = EditorWidget(self)
        layout.addWidget(self.editorWidget)
        self.setLayout(layout)
    
    def updateState(self):
        self.editorWidget.updateState()

class AlesisVSysexApplication (QMainWindow):

    def __init__(self):
        super().__init__()
        self.device = None
        self.deviceError = None
        self.connectDevice()
        self.model = self.device.default_config() if self.device else AlesisV()
        self.initWindow()

    def connectDevice(self):
        try:
            self.device = AlesisDevice.device_factory()
            self.deviceError = None
        except Exception as e:
            self.device = None
            self.deviceError = str(e)
        return self.device is not None

    def requireDevice(self):
        if self.device is not None or self.connectDevice():
            return True
        QMessageBox.warning(self, 'No MIDI Device',
                            'No Alesis V-Series device is available.\n\n%s' % self.deviceError)
        self.statusBar().showMessage('No MIDI device connected.')
        return False

    def initWindow(self):
        self.setWindowTitle('Alesis V-Series SysEx Editor')
        self.initWidget()
        if self.device is None:
            self.statusBar().showMessage('No MIDI device connected. File operations are still available.')
        else:
            self.statusBar().showMessage('Ready.')
        self.show()
        
    def initWidget(self):
        self.widget = MainWidget(self)
        self.setCentralWidget(self.widget)

    def setModel(self, model):
        rebuild = type(model) is not type(self.model)
        self.model = model
        if rebuild:
            self.initWidget()
        else:
            self.widget.updateState()
        
    def saveFile(self):
        launchSaveFileDialog(self)
    
    def saveFileCallback(self, name):
        f = FileDevice(name)
        f.set_config(self.model)
        self.statusBar().showMessage("Saved configuration to '%s'." % name)
    
    def loadFile(self):
        launchLoadFileDialog(self)
        
    def loadFileCallback(self, name):
        f = FileDevice(name)
        self.setModel(f.get_config())
        self.statusBar().showMessage("Loaded configuration from '%s'." % name)
    
    def saveDevice(self):
        if not self.requireDevice():
            return
        try:
            self.device.set_config(self.model)
        except Exception as e:
            QMessageBox.critical(self, 'Device Error',
                                 'Could not save to the device:\n\n%s' % e)
            self.statusBar().showMessage('Failed to save configuration to MIDI device.')
            return
        self.statusBar().showMessage("Saved configuration to MIDI device.")
    
    def loadDevice(self):
        if not self.requireDevice():
            return
        try:
            model = self.device.get_config()
        except Exception as e:
            QMessageBox.critical(self, 'Device Error',
                                 'Could not load from the device:\n\n%s' % e)
            self.statusBar().showMessage('Failed to load configuration from MIDI device.')
            return
        self.setModel(model)
        self.statusBar().showMessage(f"Loaded configuration from MIDI port {self.device.ioport_name}.")

    def resetDefaults(self):
        answer = QMessageBox.question(
            self, 'Reset To Defaults',
            'Reset all settings in the editor to their defaults?\n\n'
            'The device itself is not changed until you press "Save To Device".',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer != QMessageBox.Yes:
            return
        self.setModel(type(self.model)())
        self.statusBar().showMessage('Reset to defaults. Press "Save To Device" to apply them.')

