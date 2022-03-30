from PyQt5 import QtWidgets as qtw

def errorbox(msg):
    errorbox = qtw.QMessageBox()
    errorbox.setIcon(qtw.QMessageBox.Critical)
    errorbox.setText(f"{msg}")
    errorbox.setWindowTitle("ERROR")
    errorbox.exec_()
