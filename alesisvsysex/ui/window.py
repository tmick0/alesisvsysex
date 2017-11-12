from PyQt5.QtWidgets import *
from alesisvsysex.protocol.model import AlesisV
from alesisvsysex.ui.components import *

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

class ContainerWidget (QWidget):

    def __init__(self):
        super().__init__()
        
    def getModel(self):
        p = self.parent()
        while not isinstance(p, EditorWidget):
            p = p.parent()
        return p.getModel()

class EditorWidget (QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initLayout()
        
    def initLayout(self):
    
        pane1l = QHBoxLayout()
        pane1l.addWidget(BasicWidget(self, "Keys", 'keys'))
        pane1l.addWidget(BasicWidget(self, "Pitch Wheel", 'pwheel'))
        pane1l.addWidget(BasicWidget(self, "Mod Wheel", 'mwheel'))
        pane1l.addWidget(BasicWidget(self, "Sustain", 'sustain'))
        
        pane1 = ContainerWidget()
        pane1.setLayout(pane1l)
        
        pane2l = QVBoxLayout()
        pane2l.addWidget(CompoundWidget(self, "Knobs", 'knobs'))
        pane2l.addWidget(CompoundWidget(self, "Buttons", 'buttons'))
        
        pane2 = ContainerWidget()
        pane2.setLayout(pane2l)
        
        pane3l = QVBoxLayout()
        pane3l.addWidget(CompoundWidget(self, "Pads", 'pads'))
        
        pane3 = ContainerWidget()
        pane3.setLayout(pane3l)
        
        self.addTab(pane1, "Keys / Wheels / Sustain")
        self.addTab(pane2, "Knobs / Buttons")
        self.addTab(pane3, "Pads")

    def getModel(self):
        return self.parentWidget().parentWidget().model

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

