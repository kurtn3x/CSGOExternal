import time
import os.path
import sys
import pymem
import configparser
from ctypes import windll
from keyboard import is_pressed
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from ast import literal_eval

from settings.mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer
from offsets.offsets import *
from offsets.update_offsets import update_offsets
from funcs.bunnyhop import Bhop, AutoStrafe
from funcs.rcs import rcse
from classes.Classes import Vector, Color, f2b
from settings.guistuff import errorbox

k32 = windll.kernel32


class WindowThread(QThread):
    update_progress = pyqtSignal(str)

    def send_signal(self):
        self.update_progress.emit("press")

    def run(self):
        while True:
            k32.Sleep(50)
            if is_pressed('insert'):
                self.send_signal()
                k32.Sleep(200)


class MainThread(QThread):
    def __init__(self, pm, client):
        super().__init__()
        # Visuals Settings
        self.glow_enabled = 0
        self.glow_manager = pm.read_int(client + dwGlowObjectManager)
        self.glow_team = 0
        self.glow_enemy = 0
        self.glow_color_team = Color(0.0, 0.0, 255.0, 0.0)
        self.glow_color_enemy = Color(255.0, 0.0, 0.0, 0.0)

        # Misc Settings
        self.bunnyhop_enabled = 0
        self.Autostrafe = 0
        self.OldViewangle = 0

        # Put rcs here ?????
        self.rcs_enabled = 0

    def update_glow_color_team(self, color):
        self.glow_color_team = color

    def update_glow_color_enemy(self, color):
        self.glow_color_enemy = color

    def toogle_glow(self):
        if self.glow_enabled:
            self.glow_enabled = 0
        else:
            self.glow_enabled = 1

    def toogle_glow_team(self):
        if self.glow_team:
            self.glow_team = 0
        else:
            self.glow_team = 1

    def toogle_glow_enemy(self):
        if self.glow_enemy:
            self.glow_enemy = 0
        else:
            self.glow_enemy = 1

    def toogle_rcs(self):
        if self.rcs_enabled:
            self.rcs_enabled = 0
        else:
            self.rcs_enabled = 1

    def toogle_bunnyhop(self):
        if self.bunnyhop_enabled:
            self.bunnyhop_enabled = 0
        else:
            self.bunnyhop_enabled = 1

    def toogle_autostrafe(self):
        if self.Autostrafe:
            self.Autostrafe = 0
        else:
            self.Autostrafe = 1

    def run(self):
        oldpunch = Vector(0, 0, 0)
        newrcs = Vector(0, 0, 0)
        punch = Vector(0, 0, 0)
        rcs = Vector(0, 0, 0)
        while True:
            time.sleep(0.001)
            if pm.read_int(engine_pointer + dwClientState_State) == 6:
                try:
                    local_player = pm.read_uint(client + dwLocalPlayer)
                    local_player_team = pm.read_int(local_player + m_iTeamNum)
                    if self.bunnyhop_enabled and is_pressed("space"):
                        Bhop(pm, client, local_player)

                        if self.Autostrafe:  # Autostrafe
                            y_angle = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                            y_angle = AutoStrafe(pm, client, local_player, y_angle, self.OldViewangle)
                            self.OldViewangle = y_angle

                    if self.glow_enabled:
                        glow(pm, client, self.glow_manager, local_player_team, self.glow_enemy,
                             self.glow_team, self.glow_color_team, self.glow_color_enemy)

                    if self.rcs_enabled:
                        oldpunch = rcse(pm, local_player, engine_pointer, oldpunch, newrcs, punch, rcs)
                except Exception as e:
                    print(e)
                    continue



class AimbotThread(QThread):
    def __init__(self):
        super().__init__()
        self.FOV = 1
        self.Aimspots = [0, 0, 0, 0, 0]
        self.Spotted = 0
        self.enabled = 0
        self.Smooth = 0
        self.Smoothvalue = 1
        self.IndexToAimspot = {0: 8, 1: 6, 2: 4, 3: 1, 4: 3}
        self.local_player = LocalPlayer(pm, client, engine_pointer, engine)

    def update_fov(self, fov):
        self.FOV = fov

    def update_aimspot(self, aimspot):
        self.Aimspots = aimspot

    def toogle_enabled(self):
        if self.enabled:
            self.enabled = 0
        else:
            self.enabled = 1

    def toogle_spotted(self):
        if self.Spotted:
            self.Spotted = 0
        else:
            self.Spotted = 1

    def toogle_smooth(self):
        if self.Smooth:
            self.Smooth = 0
        else:
            self.Smooth = 1

    def change_smooth_value(self, val):
        self.Smoothvalue = val

    def update_localplayer(self):
        self.local_player.get()

    def run(self):
        while True:
            time.sleep(0.0000000000001)
            try:
                if pm.read_int(engine_pointer + dwClientState_State) == 6:
                    if self.enabled:
                        self.local_player.aim_at(self.Spotted, self.FOV, self.Aimspots,
                                                 pm.read_int(engine_pointer + dwClientState_MaxPlayer), self.Smooth,
                                                 self.Smoothvalue)
            except Exception as e:
                print(e)
                continue


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainwindow_ui = Ui_MainWindow()
        self.mainwindow_ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        path = os.path.join("settings", "body.jpg")
        self.mainwindow_ui.label_3.setPixmap(QPixmap(path))
        self.popups = []

        self.WindowManager = WindowThread()
        self.WindowManager.start()
        self.WindowManager.update_progress.connect(self.open_close)

        self.mainthread = MainThread(pm, client)
        self.mainthread.start()

        self.aimbot = AimbotThread()
        self.aimbot.start()

        # Aimbot
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.aimbotapplyButton.clicked.connect(lambda: self.fov_slider_set_value(
            self.mainwindow_ui.fovLineEdit.text()))
        self.mainwindow_ui.spottedCheckBox.stateChanged.connect(self.toogle_spotted)
        self.mainwindow_ui.rcsCheckBox.stateChanged.connect(self.toogle_rcs)
        self.mainwindow_ui.headCheckBox.stateChanged.connect(self.aimspot_head)
        self.mainwindow_ui.upperbodyCheckBox.stateChanged.connect(self.aimspot_uppbody)
        self.mainwindow_ui.lowerbodyCheckBox.stateChanged.connect(self.aimspot_lowbody)
        self.mainwindow_ui.legsCheckBox.stateChanged.connect(self.aimspot_leg)
        self.mainwindow_ui.leftarmCheckBox.stateChanged.connect(self.aimspot_arms)
        self.mainwindow_ui.smoothSlider.valueChanged.connect(self.change_smooth_value)
        self.mainwindow_ui.smoothCheckBox.stateChanged.connect(self.toogle_smooth)
        # Head, upper body, lower body, legs, arms
        self.Aimspots = [0, 0, 0, 0, 0]

        # Visuals
        self.mainwindow_ui.enableglowCheckBox.stateChanged.connect(self.toogle_glow)
        self.mainwindow_ui.enableglowteamCheckBox.stateChanged.connect(self.glow_team)
        self.mainwindow_ui.enableglowenemyCheckBox.stateChanged.connect(self.glow_enemy)
        self.mainwindow_ui.colorpickerGlowTeam.clicked.connect(lambda: self.pick_color("glowteam"))
        self.mainwindow_ui.colorpickerGlowEnemy.clicked.connect(lambda: self.pick_color("glowenemy"))
        self.glow_color_team = Color(0, 0, 255, 1)
        self.glow_color_enemy = Color(255, 0, 0, 1)

        self.mainwindow_ui.enablechamsCheckBox.stateChanged.connect(self.toogle_chams)
        self.mainwindow_ui.enablechamsteamCheckBox.stateChanged.connect(self.update_chams)
        self.mainwindow_ui.enablechamsenemyCheckBox.stateChanged.connect(self.update_chams)
        self.mainwindow_ui.colorpickerChamsTeam.clicked.connect(lambda: self.pick_color("chamsteam"))
        self.mainwindow_ui.colorpickerChamsEnemy.clicked.connect(lambda: self.pick_color("chamsenemy"))
        self.chams_enabled = 0
        self.chams_color_team = Color(0, 0, 255, 1)
        self.chams_color_enemy = Color(255, 0, 0, 1)
        self.brightchams = 0
        self.brightchams_value = 0
        self.mainwindow_ui.enablebrightchamsCheckbox.stateChanged.connect(self.toogle_brightchams)
        self.mainwindow_ui.chamsbrightnessSlider.valueChanged.connect(self.update_brightchams)

        self.mainwindow_ui.fovchangerCheckBox.stateChanged.connect(self.toogle_fov_changer)
        self.mainwindow_ui.fovchangerSlider.valueChanged.connect(self.change_fov_changer_value)
        self.fovchanger_enabled = 0
        self.fovchanger_value = 90.0

        self.mainwindow_ui.enablenightmodeCheckBox.stateChanged.connect(self.toogle_nightmode)
        self.mainwindow_ui.nightmodeSlider.valueChanged.connect(self.update_nightmode)

        self.nightmode_enabled = 0
        self.nightmode_value = 0.1

        # Misc
        self.mainwindow_ui.enablebunnyhopCheckBox.stateChanged.connect(self.toogle_bhop)
        self.mainwindow_ui.enableautostrafeCheckBox.stateChanged.connect(self.toogle_autostrafe)
        self.mainwindow_ui.nohandsCheckBox.stateChanged.connect(self.toogle_nohands)
        self.nohands_enabled = 0

        self.mainwindow_ui.saveconfigButton.clicked.connect(self.save_config)
        self.mainwindow_ui.loadconfigButton.clicked.connect(self.load_config)
        self.mainwindow_ui.updateloadconfigButton.clicked.connect(self.update_loaded_configs)

    def toogle_nohands(self):
        if self.nohands_enabled:
            self.nohands_enabled = 0
            tt = 0
            local_player = pm.read_uint(client + dwLocalPlayer)
            while tt < 5000:
                pm.write_int(local_player + 0x258, 100)
                tt += 1
        else:
            self.nohands_enabled = 1
            tt = 0
            local_player = pm.read_uint(client + dwLocalPlayer)
            while tt < 5000:
                pm.write_int(local_player + 0x258, 0)
                tt += 1

    def toogle_nightmode(self):
        if self.nightmode_enabled:
            self.nightmode_enabled = 0
        else:
            self.nightmode_enabled = 1

    def update_nightmode(self, Brightness):
        Brightness = float(Brightness / 100)
        print(Brightness)
        print(self.nightmode_enabled)
        if self.nightmode_enabled:
            for i in range(0, 2048):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:

                    entity_id = pm.read_int(pm.read_int(pm.read_int(pm.read_int(entity + 0x8) + 2 * 0x4) + 0x1) + 20)

                    if entity_id != 69:
                        continue

                    pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                    pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                    pm.write_float(entity + m_flCustomAutoExposureMin, Brightness)
                    pm.write_float(entity + m_flCustomAutoExposureMax, Brightness)
        else:
            for i in range(0, 2048):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:
                    entityclass = pm.read_int(pm.read_int(pm.read_int(pm.read_int(entity + 0x8) + 2 * 0x4) + 0x1) + 20)
                    if entityclass != 69:
                        continue

                    pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                    pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                    pm.write_float(entity + m_flCustomAutoExposureMin, 1.2)
                    pm.write_float(entity + m_flCustomAutoExposureMax, 1.2)

    def toogle_brightchams(self):
        if self.brightchams:
            self.brightchams = 0
            self.update_brightchams(self.brightchams_value)
        else:
            self.brightchams = 1
            self.update_brightchams(self.brightchams_value)

    def pick_color(self, x):
        print("www")
        if x == "glowteam":
            glowteam_colorpicker = QColorDialog()
            glowteam_colorpicker.setWindowTitle("Colorpicker Glow Team")
            self.popups.append(glowteam_colorpicker)
            glowteam_colorpicker.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
            color = glowteam_colorpicker.getColor(parent=self, title="Glow Team Color")
            self.mainwindow_ui.glowteamcolorLabel.setText(f"R: {color.red()} G: {color.green()} B: {color.blue()}")
            self.mainthread.update_glow_color_team(Color(color.red(), color.green(), color.blue(), 1))

        elif x == "glowenemy":
            glowenemy_colorpicker = QColorDialog()
            glowenemy_colorpicker.setWindowTitle("Colorpicker Glow Enemy")
            self.popups.append(glowenemy_colorpicker)
            glowenemy_colorpicker.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
            color = glowenemy_colorpicker.getColor(parent=self, title="Glow Enemy Color")
            self.mainwindow_ui.glowenemycolorLabel.setText(f"R: {color.red()} G: {color.green()} B: {color.blue()}")
            self.mainthread.update_glow_color_enemy(Color(color.red(), color.green(), color.blue(), 1))

        elif x == "chamsteam":
            chamsteam_colorpicker = QColorDialog()
            chamsteam_colorpicker.setWindowTitle("Colorpicker Chams Team")
            self.popups.append(chamsteam_colorpicker)
            chamsteam_colorpicker.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
            color = chamsteam_colorpicker.getColor(parent=self, title="Chams Team Color")
            self.mainwindow_ui.chamsteamcolorLabel.setText(f"R: {color.red()} G: {color.green()} B: {color.blue()}")
            self.chams_color_team = Color(color.red(), color.green(), color.blue(), 1)
            self.update_chams()

        elif x == "chamsenemy":
            print("llll")
            chamsenemy_colorpicker = QColorDialog()
            chamsenemy_colorpicker.setWindowTitle("Colorpicker Chams Enemy")
            self.popups.append(chamsenemy_colorpicker)
            chamsenemy_colorpicker.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
            color = chamsenemy_colorpicker.getColor(parent=self, title="Chams Enemy Color")
            self.mainwindow_ui.chamsenemycolorLabel.setText(f"R: {color.red()} G: {color.green()} B: {color.blue()}")
            self.chams_color_enemy = Color(color.red(), color.green(), color.blue(), 1)
            print("4")
            self.update_chams()

    def toogle_chams(self):
        if self.chams_enabled:
            self.chams_enabled = 0
            self.update_chams()
        else:
            self.chams_enabled = 1
            self.update_chams()

    def toogle_smooth(self):
        self.aimbot.toogle_smooth()

    def change_smooth_value(self, val):
        val = val
        self.aimbot.change_smooth_value(val)
        self.mainwindow_ui.smoothLineEdit.setText(f"{val}")

    def toogle_rcs(self):
        self.mainthread.toogle_rcs()

    def glow_team(self):
        self.mainthread.toogle_glow_team()

    def glow_enemy(self):
        self.mainthread.toogle_glow_enemy()

    def aimspot_head(self):
        if self.Aimspots[0] == 0:
            self.Aimspots[0] = 1
            self.aimspot_changed()
        else:
            self.Aimspots[0] = 0
            self.aimspot_changed()

    def aimspot_uppbody(self):
        if self.Aimspots[1] == 0:
            self.Aimspots[1] = 1
            self.aimspot_changed()
        else:
            self.Aimspots[1] = 0
            self.aimspot_changed()

    def aimspot_lowbody(self):
        if self.Aimspots[2] == 0:
            self.Aimspots[2] = 1
            self.aimspot_changed()
        else:
            self.Aimspots[2] = 0
            self.aimspot_changed()

    def aimspot_leg(self):
        if self.Aimspots[3] == 0:
            self.Aimspots[3] = 1
            self.aimspot_changed()
        else:
            self.Aimspots[3] = 0
            self.aimspot_changed()

    def aimspot_arms(self):
        if self.Aimspots[4] == 0:
            self.Aimspots[4] = 1
            self.aimspot_changed()
        else:
            self.Aimspots[4] = 0
            self.aimspot_changed()

    def aimspot_changed(self):
        self.aimbot.update_aimspot(self.Aimspots)

    def toogle_silentaim(self):
        self.aimbot.toogle_silent()

    def toogle_rage(self):
        self.aimbot.toogle_rage()

    def toogle_fov_changer(self):
        local_player = pm.read_uint(client + dwLocalPlayer)
        fov_changer = local_player + m_iDefaultFOV
        if self.fovchanger_enabled:
            self.fovchanger_enabled = 0
            pm.write_int(fov_changer, 90)
            self.mainwindow_ui.fovchangerLineEdit.setText(f"90")
            self.mainwindow_ui.fovchangerSlider.setValue(90)
            self.fovchanger_value = 90
        else:
            self.fovchanger_enabled = 1

    def change_fov_changer_value(self, fov):
        if self.fovchanger_enabled:
            local_player = pm.read_uint(client + dwLocalPlayer)
            self.mainwindow_ui.fovchangerLineEdit.setText(f"{fov}")
            fov_changer = local_player + m_iDefaultFOV
            pm.write_int(fov_changer, fov)
            self.fovchanger_value = fov

    def toogle_spotted(self):
        self.aimbot.toogle_spotted()

    def toogle_autostrafe(self):
        self.mainthread.toogle_autostrafe()

    def toogle_bhop(self):
        self.mainthread.toogle_bunnyhop()

    def fov_slider_set_value(self, val):
        try:
            val = float(val) * 10
            val = int(val)
            if 0.1 < val < 3600:
                self.mainwindow_ui.fovSlider.setValue(val)
        except ValueError:
            pass

    def update_aimbot_fov(self):
        fov = self.mainwindow_ui.fovSlider.value() / 10
        self.mainwindow_ui.fovLineEdit.setText(f"{fov}")
        self.aimbot.update_fov(fov)

    def toogle_glow(self):
        self.mainthread.toogle_glow()

    def start_aimbot(self):
        self.aimbot.toogle_enabled()

    def update_chams(self):
        print(self.chams_enabled)
        if self.chams_enabled:
            local_player = pm.read_uint(client + dwLocalPlayer)
            localTeam = pm.read_int(local_player + m_iTeamNum)
            for i in range(0, 32):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:
                    entityTeam = pm.read_uint(entity + m_iTeamNum)
                    if self.mainwindow_ui.enablechamsteamCheckBox.isChecked():
                        if entityTeam == localTeam and entityTeam != 0 and entity != local_player:
                            pm.write_uchar(entity + 112, self.chams_color_team.R)
                            pm.write_uchar(entity + 113, self.chams_color_team.G)
                            pm.write_uchar(entity + 114, self.chams_color_team.B)
                    else:
                        if entityTeam == localTeam and entityTeam != 0 and entity != local_player:
                            pm.write_uchar(entity + 112, 255)
                            pm.write_uchar(entity + 113, 255)
                            pm.write_uchar(entity + 114, 255)

                    if self.mainwindow_ui.enablechamsenemyCheckBox.isChecked():
                        print("1")
                        if entityTeam != localTeam and entityTeam != 0 and entity != local_player:
                            print("2")
                            pm.write_uchar(entity + 112, self.chams_color_enemy.R)
                            pm.write_uchar(entity + 113, self.chams_color_enemy.G)
                            pm.write_uchar(entity + 114, self.chams_color_enemy.B)
                    else:
                        if entityTeam != localTeam and entityTeam != 0 and entity != local_player:
                            print("3")
                            pm.write_uchar(entity + 112, 255)
                            pm.write_uchar(entity + 113, 255)
                            pm.write_uchar(entity + 114, 255)
        else:
            for i in range(0, 64):
                entity = pm.read_uint(client + dwEntityList + i * 0x10)
                if entity:
                    pm.write_uchar(entity + 112, 255)
                    pm.write_uchar(entity + 113, 255)
                    pm.write_uchar(entity + 114, 255)

    def update_brightchams(self, brightness):
        self.brightchams_value = brightness
        if self.brightchams:
            brightness = float(brightness)
            point = pm.read_int(engine + model_ambient_min - 0x2c)
            yourval = int(f2b(brightness), 2) ^ point
            pm.write_int(engine + model_ambient_min, yourval)
        else:
            brightness = float(0)
            point = pm.read_int(engine + model_ambient_min - 0x2c)
            yourval = int(f2b(brightness), 2) ^ point
            pm.write_int(engine + model_ambient_min, yourval)

    def open_close(self):
        if self.mainwindow_ui.tabWidget.isHidden():
            self.mainwindow_ui.tabWidget.show()
        else:
            self.mainwindow_ui.tabWidget.hide()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    def update_loaded_configs(self):
        files = os.listdir("configfiles")
        self.mainwindow_ui.loadconfigComboBox.clear()
        for file in files:
            self.mainwindow_ui.loadconfigComboBox.addItem(f"{file}")

    def load_config(self):
        config_name = self.mainwindow_ui.loadconfigComboBox.currentText()
        self.mainwindow_ui.currentconfigLabel.setText(config_name)
        path = os.path.join("configfiles", f"{config_name}")
        config = configparser.ConfigParser()
        config.read(path)
        self.aimbot.enabled = int(config["AIMBOT"]["enabled"])
        self.aimbot.FOV = float((config["AIMBOT"]["fov"]))
        self.aimbot.Aimspots = (config["AIMBOT"]["aimspots"])
        self.aimbot.Spotted = int(config["AIMBOT"]["spotted"])
        self.aimbot.Smooth = int(config["AIMBOT"]["smooth"])
        self.aimbot.Smoothvalue = int(config["AIMBOT"]["smoothvalue"])
        self.mainthread.rcs_enabled = int(config["AIMBOT"]["rcs"])
        if self.aimbot.enabled:
            self.mainwindow_ui.aimbotCheckBox.setChecked(True)
            self.aimbot.enabled = 1
        else:
            self.mainwindow_ui.aimbotCheckBox.setChecked(False)
            self.aimbot.enabled = 0

        self.mainwindow_ui.fovSlider.setValue(int(self.aimbot.FOV*10))
        self.mainwindow_ui.fovLineEdit.setText(f"{self.aimbot.FOV}")
        self.aimbot.Aimspots = literal_eval(self.aimbot.Aimspots)
        for i, item in enumerate(self.aimbot.Aimspots):
            if i == 0:
                if int(item) == 1:
                    self.mainwindow_ui.headCheckBox.setChecked(True)
                    self.aimbot.Aimspots[0] = 1
                else:
                    self.mainwindow_ui.headCheckBox.setChecked(False)
                    self.aimbot.Aimspots[0] = 0
            elif i ==1:
                if int(item) == 1:
                    self.mainwindow_ui.upperbodyCheckBox.setChecked(True)
                    self.aimbot.Aimspots[1] = 1
                else:
                    self.mainwindow_ui.upperbodyCheckBox.setChecked(False)
                    self.aimbot.Aimspots[1] = 0

            elif i ==2:
                if int(item) == 1:
                    self.mainwindow_ui.lowerbodyCheckBox.setChecked(True)
                    self.aimbot.Aimspots[2] = 1
                else:
                    self.mainwindow_ui.lowerbodyCheckBox.setChecked(False)
                    self.aimbot.Aimspots[2] = 0

            elif i ==3:
                if int(item) == 1:
                    self.mainwindow_ui.legsCheckBox.setChecked(True)
                    self.aimbot.Aimspots[3] = 1
                else:
                    self.mainwindow_ui.legsCheckBox.setChecked(False)
                    self.aimbot.Aimspots[3] = 0
            elif i ==4:
                if int(item) == 1:
                    self.mainwindow_ui.leftarmCheckBox.setChecked(True)
                    self.aimbot.Aimspots[4] = 1
                else:
                    self.mainwindow_ui.leftarmCheckBox.setChecked(False)
                    self.aimbot.Aimspots[4] = 0

        if self.aimbot.Spotted:
            self.mainwindow_ui.spottedCheckBox.setChecked(True)
            self.aimbot.Spotted = 1
        else:
            self.mainwindow_ui.spottedCheckBox.setChecked(False)
            self.aimbot.Spotted = 0

        if self.mainthread.rcs_enabled:
            self.mainwindow_ui.rcsCheckBox.setChecked(True)
            self.mainthread.rcs_enabled = 1
        else:
            self.mainwindow_ui.rcsCheckBox.setChecked(False)
            self.mainthread.rcs_enabled = 0

        if self.aimbot.Smooth:
            self.mainwindow_ui.smoothCheckBox.setChecked(True)
            self.aimbot.Smooth = 1
        else:
            self.mainwindow_ui.smoothCheckBox.setChecked(False)
            self.mainthread.rcs_enabled = 0

        self.mainwindow_ui.smoothSlider.setValue(int(self.aimbot.Smoothvalue))
        self.mainwindow_ui.smoothLineEdit.setText(f"{self.aimbot.Smoothvalue}")

        self.mainthread.glow_enabled = int(config["VISUAL"]["glow_enabled"])
        self.mainthread.glow_team = int(config["VISUAL"]["glow_team"])
        self.mainthread.glow_enemy  = int(config["VISUAL"]["glow_enemy"])
        tm = literal_eval(config["VISUAL"]["glow_team_color"])
        self.mainthread.update_glow_color_team(Color(tm[0], tm[1], tm[2], tm[3]))
        tm = literal_eval(config["VISUAL"]["glow_enemy_color"])
        self.mainthread.update_glow_color_team(Color(tm[0], tm[1], tm[2], tm[3]))
        if self.mainthread.glow_enabled:
            self.mainwindow_ui.enableglowCheckBox.setChecked(True)
            self.mainthread.glow_enabled = 1
        else:
            self.mainwindow_ui.enableglowCheckBox.setChecked(False)
            self.mainthread.glow_enabled = 0

        if self.mainthread.glow_team:
            self.mainwindow_ui.enableglowteamCheckBox.setChecked(True)
            self.mainthread.glow_team = 1
        else:
            self.mainwindow_ui.enableglowteamCheckBox.setChecked(False)
            self.mainthread.glow_team = 0

        if self.mainthread.glow_enemy:
            self.mainwindow_ui.enableglowenemyCheckBox.setChecked(True)
            self.mainthread.glow_enemy = 1
        else:
            self.mainwindow_ui.enableglowenemyCheckBox.setChecked(False)
            self.mainthread.glow_enemy = 0

        self.chams_enabled = int(config["VISUAL"]["chams_enabled"])
        if self.chams_enabled:
            self.mainwindow_ui.enablechamsCheckBox.setChecked(True)
            self.chams_enabled = 1
        else:
            self.mainwindow_ui.enablechamsCheckBox.setChecked(False)
            self.chams_enabled = 0

        tmp = int(config["VISUAL"]["chams_team"])
        if tmp:
            self.mainwindow_ui.enablechamsteamCheckBox.setChecked(True)
        else:
            self.mainwindow_ui.enablechamsteamCheckBox.setChecked(False)

        tmp = int(config["VISUAL"]["chams_enemy"])
        if tmp:
            self.mainwindow_ui.enablechamsenemyCheckBox.setChecked(True)
        else:
            self.mainwindow_ui.enablechamsenemyCheckBox.setChecked(False)
        tm = literal_eval(config["VISUAL"]["chams_team_color"])
        self.chams_color_team = Color(tm[0], tm[1], tm[2], tm[3])
        tm = literal_eval(config["VISUAL"]["chams_enemy_color"])
        self.chams_color_enemy = Color(tm[0], tm[1], tm[2], tm[3])
        self.update_chams()
        self.nightmode_enabled = int(config["VISUAL"]["nightmode_enabled"])
        self.nightmode_value = float(config["VISUAL"]["nightmodevalue"])
        self.brightchams = int(config["VISUAL"]["brightmodels_enabled"])
        self.brightchams_value = int(config["VISUAL"]["brightmodels_value"])
        self.fovchanger_enabled = int(config["VISUAL"]["fovchanger_enabled"])
        self.fovchanger_value = int(config["VISUAL"]["fovchanger_value"])

        if self.nightmode_enabled:
            self.mainwindow_ui.enablenightmodeCheckBox.setChecked(True)
            self.nightmode_enabled = 1
            self.update_nightmode(self.nightmode_value * 100)
        else:
            self.mainwindow_ui.enablenightmodeCheckBox.setChecked(False)
            self.nightmode_enabled = 0

        if self.brightchams:
            self.mainwindow_ui.enablebrightchamsCheckbox.setChecked(True)
            self.mainwindow_ui.chamsbrightnessSlider.setValue(self.brightchams_value)
            print(self.brightchams_value)
            self.brightchams = 1
            self.update_brightchams(self.brightchams_value)

        else:
            self.mainwindow_ui.enablenightmodeCheckBox.setChecked(False)
            self.brightchams = 0

        if self.fovchanger_enabled:
            x = self.fovchanger_value
            self.mainwindow_ui.fovchangerCheckBox.setChecked(True)
            self.mainwindow_ui.fovchangerSlider.setValue(x)
            self.fovchanger_enabled = 1
            self.mainwindow_ui.fovchangerLineEdit.setText(f"{x}")
        else:
            self.mainwindow_ui.fovchangerCheckBox.setChecked(False)
            self.fovchanger_enabled = 0

        self.mainthread.bunnyhop_enabled = int(config["MISC"]["bunnyhop_enabled"])
        if self.mainthread.bunnyhop_enabled:
            self.mainwindow_ui.enablebunnyhopCheckBox.setChecked(True)
            self.mainthread.bunnyhop_enabled = 1
        else:
            self.mainwindow_ui.enablebunnyhopCheckBox.setChecked(False)
            self.mainthread.bunnyhop_enabled = 0

        self.mainthread.Autostrafe = int(config["MISC"]["bunnyhop_autostrafe"])
        if self.mainthread.Autostrafe:
            self.mainwindow_ui.enableautostrafeCheckBox.setChecked(True)
            self.mainthread.Autostrafe = 1
        else:
            self.mainwindow_ui.enableautostrafeCheckBox.setChecked(False)
            self.mainthread.Autostrafe = 0

        self.nohands_enabled = int(config["MISC"]["nohands_enabled"])
        if self.nohands_enabled:
            self.nohands_enabled = 0
            self.mainwindow_ui.nohandsCheckBox.setChecked(True)
        else:
            self.nohands_enabled = 1
            self.mainwindow_ui.nohandsCheckBox.setChecked(False)

    def save_config(self):
        name = self.mainwindow_ui.saveconfiglineEdit.text()
        config = configparser.ConfigParser()
        config["AIMBOT"] = {"enabled": self.aimbot.enabled, "fov": self.aimbot.FOV, "aimspots": self.aimbot.Aimspots,
                            "spotted": self.aimbot.Spotted, "rcs" : self.mainthread.rcs_enabled,
                            "smooth": self.aimbot.Smooth, "smoothvalue": self.aimbot.Smoothvalue}

        if self.mainwindow_ui.enablechamsenemyCheckBox.isChecked():
            chams_enemy = 1
        else:
            chams_enemy = 0
        if self.mainwindow_ui.enablechamsteamCheckBox.isChecked():
            chams_team = 1
        else:
            chams_team = 0

        config["VISUAL"] = {"glow_enabled": self.mainthread.glow_enabled, "glow_team": self.mainthread.glow_team,
                            "glow_enemy": self.mainthread.glow_enemy,
                            "glow_team_color": [self.mainthread.glow_color_team.R, self.mainthread.glow_color_team.G,
                                                self.mainthread.glow_color_team.B, self.mainthread.glow_color_team.A],
                            "glow_enemy_color": [self.mainthread.glow_color_enemy.R, self.mainthread.glow_color_enemy.G,
                                                 self.mainthread.glow_color_enemy.B,
                                                 self.mainthread.glow_color_enemy.A],
                            "chams_enabled": self.chams_enabled, "chams_team": chams_team, "chams_enemy": chams_enemy,
                            "chams_team_color": [self.chams_color_team.R, self.chams_color_team.G,
                                                 self.chams_color_team.B, self.chams_color_team.A],
                            "chams_enemy_color": [self.chams_color_enemy.R, self.chams_color_enemy.G,
                                                  self.chams_color_enemy.B, self.chams_color_enemy.A],
                            "nightmode_enabled": self.nightmode_enabled, "nightmodevalue": self.nightmode_value,
                            "brightmodels_enabled": self.brightchams, "brightmodels_value": self.brightchams_value,
                            "fovchanger_enabled": self.fovchanger_enabled, "fovchanger_value": self.fovchanger_value}
        config["MISC"] = {"bunnyhop_enabled": self.mainthread.bunnyhop_enabled,
                          "bunnyhop_autostrafe": self.mainthread.Autostrafe, "nohands_enabled": self.nohands_enabled}
        path = os.path.join("configfiles", f"{name}.ini")
        with open(path, 'w') as configfile:
            config.write(configfile)
        self.mainwindow_ui.currentconfigLabel.setText(f"{name}")


def run():
    global pm
    global client
    global engine
    global engine_pointer
    global game_state
    app = QApplication(["matplotlib"])
    try:
        pm = pymem.Pymem("csgo.exe")
    except pymem.exception.ProcessNotFound:
        errorbox("Please start csgo first.")
    else:
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        engine_pointer = pm.read_uint(engine + dwClientState)
        mainwindow = MainWindow()
        update_offsets()
        mainwindow.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    run()
