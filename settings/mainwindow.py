# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(729, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 731, 461))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.tabWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI Semilight")
        font.setPointSize(14)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.fovSlider = QtWidgets.QSlider(self.tab)
        self.fovSlider.setGeometry(QtCore.QRect(50, 100, 571, 21))
        self.fovSlider.setMinimum(1)
        self.fovSlider.setMaximum(1800)
        self.fovSlider.setPageStep(360)
        self.fovSlider.setProperty("value", 1)
        self.fovSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fovSlider.setInvertedAppearance(False)
        self.fovSlider.setInvertedControls(False)
        self.fovSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.fovSlider.setTickInterval(1)
        self.fovSlider.setObjectName("fovSlider")
        self.fovLabel = QtWidgets.QLabel(self.tab)
        self.fovLabel.setGeometry(QtCore.QRect(10, 60, 131, 31))
        self.fovLabel.setObjectName("fovLabel")
        self.aimbotCheckBox = QtWidgets.QCheckBox(self.tab)
        self.aimbotCheckBox.setGeometry(QtCore.QRect(20, 10, 201, 31))
        self.aimbotCheckBox.setObjectName("aimbotCheckBox")
        self.fovLineEdit = QtWidgets.QLineEdit(self.tab)
        self.fovLineEdit.setGeometry(QtCore.QRect(70, 60, 61, 31))
        self.fovLineEdit.setObjectName("fovLineEdit")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 140, 111, 41))
        self.label.setObjectName("label")
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(0, 50, 691, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.spottedCheckBox = QtWidgets.QCheckBox(self.tab)
        self.spottedCheckBox.setGeometry(QtCore.QRect(20, 180, 111, 41))
        self.spottedCheckBox.setObjectName("spottedCheckBox")
        self.rcsCheckBox = QtWidgets.QCheckBox(self.tab)
        self.rcsCheckBox.setGeometry(QtCore.QRect(20, 220, 81, 31))
        self.rcsCheckBox.setObjectName("rcsCheckBox")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 41, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(630, 90, 51, 41))
        self.label_5.setObjectName("label_5")
        self.smoothCheckBox = QtWidgets.QCheckBox(self.tab)
        self.smoothCheckBox.setGeometry(QtCore.QRect(20, 250, 121, 31))
        self.smoothCheckBox.setObjectName("smoothCheckBox")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(520, 130, 161, 321))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.upperbodyCheckBox = QtWidgets.QCheckBox(self.tab)
        self.upperbodyCheckBox.setGeometry(QtCore.QRect(590, 200, 21, 17))
        self.upperbodyCheckBox.setText("")
        self.upperbodyCheckBox.setTristate(False)
        self.upperbodyCheckBox.setObjectName("upperbodyCheckBox")
        self.lowerbodyCheckBox = QtWidgets.QCheckBox(self.tab)
        self.lowerbodyCheckBox.setGeometry(QtCore.QRect(590, 260, 21, 17))
        self.lowerbodyCheckBox.setText("")
        self.lowerbodyCheckBox.setTristate(False)
        self.lowerbodyCheckBox.setObjectName("lowerbodyCheckBox")
        self.headCheckBox = QtWidgets.QCheckBox(self.tab)
        self.headCheckBox.setGeometry(QtCore.QRect(590, 150, 21, 17))
        self.headCheckBox.setText("")
        self.headCheckBox.setTristate(False)
        self.headCheckBox.setObjectName("headCheckBox")
        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(0, 120, 691, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.smoothSlider = QtWidgets.QSlider(self.tab)
        self.smoothSlider.setGeometry(QtCore.QRect(50, 290, 311, 21))
        self.smoothSlider.setMinimum(1)
        self.smoothSlider.setMaximum(100)
        self.smoothSlider.setPageStep(100)
        self.smoothSlider.setProperty("value", 1)
        self.smoothSlider.setOrientation(QtCore.Qt.Horizontal)
        self.smoothSlider.setInvertedAppearance(False)
        self.smoothSlider.setInvertedControls(False)
        self.smoothSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.smoothSlider.setTickInterval(1)
        self.smoothSlider.setObjectName("smoothSlider")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 290, 41, 21))
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(370, 280, 61, 41))
        self.label_8.setObjectName("label_8")
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(470, 130, 16, 381))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.smoothLineEdit = QtWidgets.QLabel(self.tab)
        self.smoothLineEdit.setGeometry(QtCore.QRect(140, 250, 81, 21))
        self.smoothLineEdit.setObjectName("smoothLineEdit")
        self.aimbotapplyButton = QtWidgets.QPushButton(self.tab)
        self.aimbotapplyButton.setGeometry(QtCore.QRect(130, 60, 81, 41))
        self.aimbotapplyButton.setObjectName("aimbotapplyButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.enableglowCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enableglowCheckBox.setGeometry(QtCore.QRect(20, 20, 161, 31))
        self.enableglowCheckBox.setObjectName("enableglowCheckBox")
        self.fovchangerCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.fovchangerCheckBox.setGeometry(QtCore.QRect(20, 370, 141, 41))
        self.fovchangerCheckBox.setObjectName("fovchangerCheckBox")
        self.fovchangerSlider = QtWidgets.QSlider(self.tab_2)
        self.fovchangerSlider.setGeometry(QtCore.QRect(260, 380, 391, 22))
        self.fovchangerSlider.setMinimum(60)
        self.fovchangerSlider.setMaximum(160)
        self.fovchangerSlider.setProperty("value", 90)
        self.fovchangerSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fovchangerSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.fovchangerSlider.setObjectName("fovchangerSlider")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(240, 400, 31, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(640, 400, 31, 41))
        self.label_7.setObjectName("label_7")
        self.enableglowteamCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enableglowteamCheckBox.setGeometry(QtCore.QRect(180, 20, 141, 31))
        self.enableglowteamCheckBox.setObjectName("enableglowteamCheckBox")
        self.enableglowenemyCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enableglowenemyCheckBox.setGeometry(QtCore.QRect(180, 60, 91, 31))
        self.enableglowenemyCheckBox.setObjectName("enableglowenemyCheckBox")
        self.line_4 = QtWidgets.QFrame(self.tab_2)
        self.line_4.setGeometry(QtCore.QRect(0, 100, 691, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.enablechamsCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enablechamsCheckBox.setGeometry(QtCore.QRect(20, 140, 171, 31))
        self.enablechamsCheckBox.setObjectName("enablechamsCheckBox")
        self.enablechamsteamCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enablechamsteamCheckBox.setGeometry(QtCore.QRect(180, 140, 141, 31))
        self.enablechamsteamCheckBox.setObjectName("enablechamsteamCheckBox")
        self.enablechamsenemyCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enablechamsenemyCheckBox.setGeometry(QtCore.QRect(180, 180, 141, 31))
        self.enablechamsenemyCheckBox.setObjectName("enablechamsenemyCheckBox")
        self.line_6 = QtWidgets.QFrame(self.tab_2)
        self.line_6.setGeometry(QtCore.QRect(0, 240, 691, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.enablenightmodeCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.enablenightmodeCheckBox.setGeometry(QtCore.QRect(20, 320, 181, 31))
        self.enablenightmodeCheckBox.setObjectName("enablenightmodeCheckBox")
        self.nightmodeSlider = QtWidgets.QSlider(self.tab_2)
        self.nightmodeSlider.setGeometry(QtCore.QRect(260, 330, 391, 22))
        self.nightmodeSlider.setMinimum(1)
        self.nightmodeSlider.setMaximum(1500)
        self.nightmodeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.nightmodeSlider.setObjectName("nightmodeSlider")
        self.glowteamcolorLabel = QtWidgets.QLabel(self.tab_2)
        self.glowteamcolorLabel.setGeometry(QtCore.QRect(270, 11, 291, 51))
        self.glowteamcolorLabel.setObjectName("glowteamcolorLabel")
        self.glowenemycolorLabel = QtWidgets.QLabel(self.tab_2)
        self.glowenemycolorLabel.setGeometry(QtCore.QRect(270, 46, 301, 61))
        self.glowenemycolorLabel.setObjectName("glowenemycolorLabel")
        self.colorpickerGlowTeam = QtWidgets.QPushButton(self.tab_2)
        self.colorpickerGlowTeam.setGeometry(QtCore.QRect(540, 20, 131, 41))
        self.colorpickerGlowTeam.setObjectName("colorpickerGlowTeam")
        self.colorpickerGlowEnemy = QtWidgets.QPushButton(self.tab_2)
        self.colorpickerGlowEnemy.setGeometry(QtCore.QRect(540, 60, 131, 41))
        self.colorpickerGlowEnemy.setObjectName("colorpickerGlowEnemy")
        self.fovchangerLineEdit = QtWidgets.QLabel(self.tab_2)
        self.fovchangerLineEdit.setGeometry(QtCore.QRect(120, 410, 31, 31))
        self.fovchangerLineEdit.setObjectName("fovchangerLineEdit")
        self.chamsteamcolorLabel = QtWidgets.QLabel(self.tab_2)
        self.chamsteamcolorLabel.setGeometry(QtCore.QRect(270, 130, 291, 51))
        self.chamsteamcolorLabel.setObjectName("chamsteamcolorLabel")
        self.chamsenemycolorLabel = QtWidgets.QLabel(self.tab_2)
        self.chamsenemycolorLabel.setGeometry(QtCore.QRect(270, 170, 301, 51))
        self.chamsenemycolorLabel.setObjectName("chamsenemycolorLabel")
        self.colorpickerChamsTeam = QtWidgets.QPushButton(self.tab_2)
        self.colorpickerChamsTeam.setGeometry(QtCore.QRect(550, 130, 131, 41))
        self.colorpickerChamsTeam.setObjectName("colorpickerChamsTeam")
        self.colorpickerChamsEnemy = QtWidgets.QPushButton(self.tab_2)
        self.colorpickerChamsEnemy.setGeometry(QtCore.QRect(550, 170, 131, 41))
        self.colorpickerChamsEnemy.setObjectName("colorpickerChamsEnemy")
        self.enablebrightchamsCheckbox = QtWidgets.QCheckBox(self.tab_2)
        self.enablebrightchamsCheckbox.setGeometry(QtCore.QRect(20, 270, 181, 31))
        self.enablebrightchamsCheckbox.setObjectName("enablebrightchamsCheckbox")
        self.chamsbrightnessSlider = QtWidgets.QSlider(self.tab_2)
        self.chamsbrightnessSlider.setGeometry(QtCore.QRect(260, 280, 391, 22))
        self.chamsbrightnessSlider.setMaximum(100)
        self.chamsbrightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.chamsbrightnessSlider.setObjectName("chamsbrightnessSlider")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(40, 410, 101, 31))
        self.label_15.setObjectName("label_15")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.enablebunnyhopCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.enablebunnyhopCheckBox.setGeometry(QtCore.QRect(30, 30, 241, 31))
        self.enablebunnyhopCheckBox.setObjectName("enablebunnyhopCheckBox")
        self.enableautostrafeCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.enableautostrafeCheckBox.setGeometry(QtCore.QRect(60, 70, 161, 21))
        self.enableautostrafeCheckBox.setObjectName("enableautostrafeCheckBox")
        self.nohandsCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.nohandsCheckBox.setGeometry(QtCore.QRect(30, 110, 141, 31))
        self.nohandsCheckBox.setObjectName("nohandsCheckBox")
        self.saveconfiglineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.saveconfiglineEdit.setGeometry(QtCore.QRect(70, 310, 171, 41))
        self.saveconfiglineEdit.setClearButtonEnabled(False)
        self.saveconfiglineEdit.setObjectName("saveconfiglineEdit")
        self.saveconfigButton = QtWidgets.QPushButton(self.tab_3)
        self.saveconfigButton.setGeometry(QtCore.QRect(80, 360, 141, 41))
        self.saveconfigButton.setObjectName("saveconfigButton")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(80, 410, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.line_5 = QtWidgets.QFrame(self.tab_3)
        self.line_5.setGeometry(QtCore.QRect(320, 230, 20, 221))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_7 = QtWidgets.QFrame(self.tab_3)
        self.line_7.setGeometry(QtCore.QRect(0, 270, 691, 16))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(90, 240, 141, 31))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setGeometry(QtCore.QRect(440, 230, 141, 31))
        self.label_11.setObjectName("label_11")
        self.loadconfigComboBox = QtWidgets.QComboBox(self.tab_3)
        self.loadconfigComboBox.setGeometry(QtCore.QRect(390, 320, 241, 31))
        self.loadconfigComboBox.setObjectName("loadconfigComboBox")
        self.loadconfigComboBox.addItem("")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        self.label_12.setGeometry(QtCore.QRect(390, 290, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setGeometry(QtCore.QRect(30, 160, 151, 41))
        self.label_13.setObjectName("label_13")
        self.currentconfigLabel = QtWidgets.QLabel(self.tab_3)
        self.currentconfigLabel.setGeometry(QtCore.QRect(230, 160, 101, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 212, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 212, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 212, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 113, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.currentconfigLabel.setPalette(palette)
        self.currentconfigLabel.setObjectName("currentconfigLabel")
        self.updateloadconfigButton = QtWidgets.QPushButton(self.tab_3)
        self.updateloadconfigButton.setGeometry(QtCore.QRect(390, 370, 91, 41))
        self.updateloadconfigButton.setObjectName("updateloadconfigButton")
        self.loadconfigButton = QtWidgets.QPushButton(self.tab_3)
        self.loadconfigButton.setGeometry(QtCore.QRect(510, 370, 91, 41))
        self.loadconfigButton.setObjectName("loadconfigButton")
        self.label_14 = QtWidgets.QLabel(self.tab_3)
        self.label_14.setGeometry(QtCore.QRect(350, 420, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.closeCheatButton = QtWidgets.QPushButton(self.tab_3)
        self.closeCheatButton.setGeometry(QtCore.QRect(500, 20, 161, 41))
        self.closeCheatButton.setObjectName("closeCheatButton")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fovLabel.setText(_translate("MainWindow", "FOV: "))
        self.aimbotCheckBox.setToolTip(_translate("MainWindow", "Enable aimbot, required for this menu to work"))
        self.aimbotCheckBox.setText(_translate("MainWindow", "Enable Aimbot"))
        self.fovLineEdit.setToolTip(_translate("MainWindow", "you can also type in here"))
        self.fovLineEdit.setText(_translate("MainWindow", "1"))
        self.label.setText(_translate("MainWindow", "Settings"))
        self.spottedCheckBox.setToolTip(_translate("MainWindow", "Only aim when in sight, aims trough walls otherwise "))
        self.spottedCheckBox.setText(_translate("MainWindow", "Spotted"))
        self.rcsCheckBox.setToolTip(_translate("MainWindow", "RCS"))
        self.rcsCheckBox.setText(_translate("MainWindow", "RCS"))
        self.label_4.setText(_translate("MainWindow", "0.1"))
        self.label_5.setText(_translate("MainWindow", "180"))
        self.smoothCheckBox.setToolTip(_translate("MainWindow", "Smooth"))
        self.smoothCheckBox.setText(_translate("MainWindow", "Smooth"))
        self.upperbodyCheckBox.setToolTip(_translate("MainWindow", "Aimspot Upper Body"))
        self.lowerbodyCheckBox.setToolTip(_translate("MainWindow", "Aimspot Lower Body"))
        self.headCheckBox.setToolTip(_translate("MainWindow", "Aimspot Head"))
        self.label_2.setText(_translate("MainWindow", "1"))
        self.label_8.setText(_translate("MainWindow", "100"))
        self.smoothLineEdit.setText(_translate("MainWindow", "1"))
        self.aimbotapplyButton.setText(_translate("MainWindow", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Aimbot"))
        self.enableglowCheckBox.setText(_translate("MainWindow", "Enable Glow"))
        self.fovchangerCheckBox.setText(_translate("MainWindow", "FovChanger"))
        self.label_6.setText(_translate("MainWindow", "60"))
        self.label_7.setText(_translate("MainWindow", "160"))
        self.enableglowteamCheckBox.setText(_translate("MainWindow", "Team"))
        self.enableglowenemyCheckBox.setText(_translate("MainWindow", "Enemy"))
        self.enablechamsCheckBox.setText(_translate("MainWindow", "Enable Chams"))
        self.enablechamsteamCheckBox.setText(_translate("MainWindow", "Team"))
        self.enablechamsenemyCheckBox.setText(_translate("MainWindow", "Enemy"))
        self.enablenightmodeCheckBox.setToolTip(_translate("MainWindow", "Makes the whole map brighter or darker"))
        self.enablenightmodeCheckBox.setText(_translate("MainWindow", "Map Brightness"))
        self.nightmodeSlider.setToolTip(_translate("MainWindow", "Takes time to update. Wait a few sec after updating."))
        self.glowteamcolorLabel.setText(_translate("MainWindow", "R: G: B:"))
        self.glowenemycolorLabel.setText(_translate("MainWindow", "R: G: B:"))
        self.colorpickerGlowTeam.setText(_translate("MainWindow", "colorpicker"))
        self.colorpickerGlowEnemy.setText(_translate("MainWindow", "colorpicker"))
        self.fovchangerLineEdit.setText(_translate("MainWindow", "90"))
        self.chamsteamcolorLabel.setText(_translate("MainWindow", "R: G: B:"))
        self.chamsenemycolorLabel.setText(_translate("MainWindow", "R: G: B:"))
        self.colorpickerChamsTeam.setText(_translate("MainWindow", "colorpicker"))
        self.colorpickerChamsEnemy.setText(_translate("MainWindow", "colorpicker"))
        self.enablebrightchamsCheckbox.setToolTip(_translate("MainWindow", "Makes all Player models brighter"))
        self.enablebrightchamsCheckbox.setText(_translate("MainWindow", "Brightmodels"))
        self.chamsbrightnessSlider.setToolTip(_translate("MainWindow", "Brightvalue"))
        self.label_15.setText(_translate("MainWindow", "FOV:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Visuals"))
        self.enablebunnyhopCheckBox.setText(_translate("MainWindow", "Enable Bunnyhop"))
        self.enableautostrafeCheckBox.setText(_translate("MainWindow", "Autostrafe"))
        self.nohandsCheckBox.setText(_translate("MainWindow", "Nohands"))
        self.saveconfiglineEdit.setPlaceholderText(_translate("MainWindow", "Configname"))
        self.saveconfigButton.setText(_translate("MainWindow", "Save"))
        self.label_10.setText(_translate("MainWindow", "saved to configfiles folder"))
        self.label_9.setText(_translate("MainWindow", "Save Config"))
        self.label_11.setText(_translate("MainWindow", "Load Config"))
        self.loadconfigComboBox.setItemText(0, _translate("MainWindow", "default.ini"))
        self.label_12.setText(_translate("MainWindow", "has to be in configfiles folder"))
        self.label_13.setText(_translate("MainWindow", "Current Config:"))
        self.currentconfigLabel.setText(_translate("MainWindow", "Default"))
        self.updateloadconfigButton.setText(_translate("MainWindow", "Update"))
        self.loadconfigButton.setText(_translate("MainWindow", "Load"))
        self.label_14.setText(_translate("MainWindow", "press update first to show available configs"))
        self.closeCheatButton.setToolTip(_translate("MainWindow", "Closes the Cheat and tries to reset all settings to normal. Map Brightness may be off."))
        self.closeCheatButton.setText(_translate("MainWindow", "Close Cheat"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Misc"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
