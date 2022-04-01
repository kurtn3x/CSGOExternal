from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import *


def errorbox(msg):
    errorbox = qtw.QMessageBox()
    errorbox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    errorbox.setIcon(qtw.QMessageBox.Critical)
    errorbox.setText(f"{msg}")
    errorbox.setWindowTitle("ERROR")
    errorbox.exec_()


def successfullbox(msg):
    successfulbox = qtw.QMessageBox()
    successfulbox.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    successfulbox.setIcon(qtw.QMessageBox.Information)
    successfulbox.setText(f"{msg}")
    successfulbox.setWindowTitle("Successful")
    successfulbox.exec_()
