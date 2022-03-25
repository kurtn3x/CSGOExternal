import os.path
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import pymem
from settings.mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer, TargetPlayer
from offsets.offsets import *
from keyboard import is_pressed
from funcs.bunnyhop import Bhop, AutoStrafe
from ctypes import windll, pointer, c_uint32
k32 = windll.kernel32
from math import *
from funcs.aimbot import normalize_angles, calc_distance, calc_angle, Vector
from funcs.rcs import rcse


class WindowThread(QThread):
    update_progress = pyqtSignal(str)

    def send_signal(self):
        self.update_progress.emit("press")

    def run(self):
        while True:
            k32.Sleep(50)
            if is_pressed('insert'):
                self.send_signal()


class MainThread(QThread):
    def __init__(self, pm, client):
        super().__init__()
        # Visuals Settings
        self.glow_enabled = 0
        self.glow_manager = pm.read_int(client + dwGlowObjectManager)
        self.glow_team = 0
        self.glow_enemy = 0

        # Misc Settings
        self.bunnyhop_enabled = 0
        self.Autostrafe = False
        self.OldViewangle = 0

        # Put rcs here ?????
        self.rcs_enabled = 0

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
            self.Autostrafe = False
        else:
            self.Autostrafe = True

    def run(self):
        oldpunch = Vector(0, 0, 0)
        newrcs = Vector(0, 0, 0)
        punch = Vector(0, 0, 0)
        rcs = Vector(0, 0, 0)
        while True:
            time.sleep(0.00000001)
            if self.bunnyhop_enabled:
                if is_pressed("space"):
                    Bhop(pm, client, local_player)

                if self.Autostrafe:  # Autostrafe
                    y_angle = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                    y_angle = AutoStrafe(pm, client, local_player, y_angle, self.OldViewangle)
                    self.OldViewangle = y_angle
            if self.glow_enabled:
                glow(pm, client, self.glow_manager, pm.read_int(local_player + m_iTeamNum), self.glow_enemy,
                     self.glow_team)

            if self.rcs_enabled:
                oldpunch = rcse(pm, local_player, engine_pointer, oldpunch, newrcs, punch, rcs)


class AimbotThread(QThread):
    update_localpos = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.FOV = 1
        self.Aimspots = [0, 0, 0, 0, 0]
        self.Spotted = False
        self.enabled = False
        self.Wait = 150
        self.Smooth = False
        self.Smoothvalue = 1
        self.IndexToAimspot = {0: 8, 1: 6, 2: 4, 3: 1, 4: 3}
        # 8 6 4 1 3

    def update_fov(self, fov):
        self.FOV = fov

    def update_aimspot(self, aimspot):
        self.Aimspots = aimspot

    def toogle_enabled(self):
        if self.enabled:
            self.enabled = False
            self.Wait = 150
        else:
            self.enabled = True
            self.Wait = 1

    def toogle_spotted(self):
        if self.Spotted:
            self.Spotted = False
        else:
            self.Spotted = True

    def run(self):
        local_player = LocalPlayer(pm, client, engine_pointer, engine)
        local_player.get()
        while True:
            time.sleep(0.000000001)
            if is_in_game():
                if self.enabled:
                    local_player.aim_at(self.Spotted, self.FOV, self.Aimspots, get_max_clients())


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainwindow_ui = Ui_MainWindow()
        self.mainwindow_ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.WindowManager = WindowThread()
        self.WindowManager.start()
        self.WindowManager.update_progress.connect(self.open_close)
        path = os.path.join("settings", "body.jpg")
        self.mainwindow_ui.label_3.setPixmap(QPixmap(path))
        self.mainthread = MainThread(pm, client)
        self.mainthread.start()

        self.aimbot = AimbotThread()
        self.aimbot.start()
        # Head, upper body, lower body, legs, arms
        self.Aimspots = [0, 0, 0, 0, 0]
        self.fovchanger_enabled = False

        # Aimbot
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.fovLineEdit.textChanged.connect(self.fov_slider_set_value)
        self.mainwindow_ui.spottedCheckBox.stateChanged.connect(self.toogle_spotted)
        self.mainwindow_ui.rcsCheckBox.stateChanged.connect(self.toogle_rcs)
        self.mainwindow_ui.headCheckBox.stateChanged.connect(self.aimspot_head)
        self.mainwindow_ui.upperbodyCheckBox.stateChanged.connect(self.aimspot_uppbody)
        self.mainwindow_ui.lowerbodyCheckBox.stateChanged.connect(self.aimspot_lowbody)
        self.mainwindow_ui.legsCheckBox.stateChanged.connect(self.aimspot_leg)
        self.mainwindow_ui.leftarmCheckBox.stateChanged.connect(self.aimspot_arms)

        # Visuals
        self.mainwindow_ui.enableglowCheckBox.stateChanged.connect(self.toogle_glow)
        self.mainwindow_ui.enableglowteamCheckBox.stateChanged.connect(self.glow_team)
        self.mainwindow_ui.enableglowenemyCheckBox.stateChanged.connect(self.glow_enemy)
        self.mainwindow_ui.fovchangerCheckBox.stateChanged.connect(self.toogle_fov_changer)
        self.mainwindow_ui.fovchangerSlider.valueChanged.connect(self.fov_changer_change)

        # Misc
        self.mainwindow_ui.enablebunnyhopCheckBox.stateChanged.connect(self.toogle_bhop)
        self.mainwindow_ui.enableautostrafeCheckBox.stateChanged.connect(self.toogle_autostrafe)

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
        fov_changer = local_player + m_iDefaultFOV
        if self.fovchanger_enabled:
            self.fovchanger_enabled = 0
            pm.write_int(fov_changer, 90)
            self.mainwindow_ui.fovchangerLineEdit.setText(f"90")
            self.mainwindow_ui.fovchangerSlider.setValue(90)
        else:
            self.fovchanger_enabled = 1

    def fov_changer_change(self, fov):
        if self.fovchanger_enabled:
            self.mainwindow_ui.fovchangerLineEdit.setText(f"{fov}")
            fov_changer = local_player + m_iDefaultFOV
            pm.write_int(fov_changer, fov)

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
            if 0.1 < val < 360:
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


def get_max_clients():
    return pm.read_int(engine_pointer + dwClientState_MaxPlayer)


def is_in_game():
    return pm.read_int(engine_pointer + dwClientState_State) == 6


def run():
    global pm
    global client
    global engine
    global engine_pointer
    global local_player
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    cvars = pymem.process.module_from_name(pm.process_handle, 'vstdlib.dll').lpBaseOfDll
    engine_pointer = pm.read_uint(engine + dwClientState)
    local_player = pm.read_uint(client + dwLocalPlayer)
    modules = list(pm.list_modules())
    for module in modules:
        if module.name == 'vstdlib.dll':
            print(pymem.pattern.pattern_scan_module(pm.process_handle, module, b'sv_cheats'))

    app = QApplication(["matplotlib"])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
