from PyQt5.QtWidgets import QApplication
from alesisvsysex.ui.window import AlesisVSysexApplication

def main(argv):
    app = QApplication(argv)
    ex = AlesisVSysexApplication()
    return app.exec_()

