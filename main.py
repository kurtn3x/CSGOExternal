import os.path
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
from global_hotkeys import *
import pymem
from settings.mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer, TargetPlayer
from offsets.offsets import *
from keyboard import is_pressed
from funcs.bunnyhop import Bhop, AutoStrafe
from ctypes import windll, pointer, c_uint32
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


class MainThread(QThread):
    def __init__(self, pm, client):
        super().__init__()
        # Visuals Settings
        self.glow_enabled = 0
        self.glow_manager = pm.read_int(client + dwGlowObjectManager)

        # Misc Settings
        self.bunnyhop_enabled = 0
        self.Autostrafe = False
        self.OldViewangle = 0


        # Put rcs here ?????
    def toogle_glow(self):
        if self.glow_enabled:
            self.glow_enabled = 0
        else:
            self.glow_enabled = 1

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
        while True:
            time.sleep(0.0004)
            if self.bunnyhop_enabled:
                if is_pressed("space"):
                    Bhop(pm, client, Local_Player)

                if self.Autostrafe:  # Autostrafe
                    y_angle = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                    y_angle = AutoStrafe(pm, client, Local_Player, y_angle, self.OldViewangle)
                    self.OldViewangle = y_angle
            if self.glow_enabled:
                glow(pm, client, self.glow_manager)


class AimbotThread(QThread):
    update_localpos = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.FOV = 1
        # Head, Upper Body, Lower Body, Arms, Legs
        self.Aimspots = [0, 0, 0, 0, 0]
        self.Spotted = False
        self.Silent = False
        self.RCS = False
        self.Rage = False
        self.enabled = False
        self.Wait = 150
        self.Smooth = False
        self.Smoothvalue = 1
        self.closest = False

    def update_fov(self, fov):
        self.FOV = fov

    def update_aimspot(self, aimspot):
        self.Aimspots = aimspot

    def toogle_closest(self):
        if self.closest:
            self.closest = False
        else:
            self.closest = True

    def toogle_enabled(self):
        if self.enabled:
            self.enabled = False
            if self.RCS:
                self.Wait = 1
            else:
                self.Wait = 150
        else:
            self.enabled = True
            self.Wait = 1

    def toogle_silent(self):
        if self.Silent:
            self.Silent = False
        else:
            self.Silent = True

    def toogle_spotted(self):
        if self.Spotted:
            self.Spotted = False
        else:
            self.Spotted = True

    def toogle_rcs(self):
        if self.RCS:
            self.RCS = False
            if self.enabled:
                self.Wait = 1
            else:
                self.Wait = 150
        else:
            self.RCS = True
            self.Wait = 1

    def toogle_rage(self):
        if self.Rage:
            self.Rage = False
        else:
            self.Rage = True

    def run(self):
        local_player = LocalPlayer(pm, client, engine_pointer, engine)
        local_player.get()
        while True:
            k32.Sleep(self.Wait)
            print(self.Wait)
            if self.enabled:
                old_distance_x = 111111111
                old_distance_y = 111111111

                for i in range(32):
                    target_player = pm.read_uint(client + dwEntityList + i * 0x10)
                    target_player = TargetPlayer(target_player, self.Aimspots, pm)

                    if not target_player.TargetPlayer:
                        continue

                    local_player.get_team()
                    target_player.get_team()
                    local_player.get_health()
                    target_player.get_health()
                    target_player.get_dormant()

                    if target_player.Team == local_player.Team:
                        continue
                    if target_player.Health < 1 or local_player.Health < 1:
                        continue
                    if not local_player.LocalPlayer:
                        continue
                    if local_player.LocalPlayer == target_player.TargetPlayer:
                        continue
                    if target_player.Dormant:
                        continue
                    try:
                        old_distance_x, old_distance_y = local_player.aim_at(target_player, old_distance_x,
                                                                             old_distance_y, self.Spotted,
                                                                             self.FOV, self.RCS,
                                                                             self.Smooth, self.Smoothvalue
                                                                             )
                    except TypeError:
                        continue
            else:
                if self.RCS and pm.read_int(local_player.LocalPlayer + m_iShotsFired) > 1:
                    local_player.get_view_offset()
                    local_player.get_punch()
                    pm.write_float(engine_pointer + dwClientState_ViewAngles,
                                   local_player.ViewOffset.x - (local_player.PunchX * 2))
                    pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4,
                                   local_player.ViewOffset.y - (local_player.PunchY * 2))


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

        # Aimbot
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.fovLineEdit.textChanged.connect(self.fov_slider_set_value)
        self.mainwindow_ui.aimspotBox.activated.connect(self.update_aimbot_aimspot)
        self.mainwindow_ui.spottedCheckBox.stateChanged.connect(self.toogle_spotted)
        self.mainwindow_ui.rcsCheckBox.stateChanged.connect(self.toogle_rcs)
        self.mainwindow_ui.headCheckBox.stateChanged.connect(self.aimspot_head)
        self.mainwindow_ui.upperbodyCheckBox.stateChanged.connect(self.aimspot_uppbody)
        self.mainwindow_ui.lowerbodyCheckBox.stateChanged.connect(self.aimspot_lowbody)
        self.mainwindow_ui.legsCheckBox.stateChanged.connect(self.aimspot_leg)
        self.mainwindow_ui.leftarmCheckBox.stateChanged.connect(self.aimspot_arms)


        # Visuals
        self.mainwindow_ui.enableglowCheckBox.stateChanged.connect(self.toogle_glow)
        self.mainwindow_ui.fovchangerSlider.valueChanged.connect(self.fov_changer)

        # Misc
        self.mainwindow_ui.enablebunnyhopCheckBox.stateChanged.connect(self.toogle_bhop)
        self.mainwindow_ui.enableautostrafeCheckBox.stateChanged.connect(self.toogle_autostrafe)

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

    def toogle_rcs(self):
        self.aimbot.toogle_rcs()

    def fov_changer(self, fov):
        if self.mainwindow_ui.fovchangerCheckBox.isChecked():
            self.mainwindow_ui.fovchangerLineEdit.setText(f"{fov}")
            fov_changer = Local_Player + m_iDefaultFOV
            pm.write_int(fov_changer, fov)

    def run(self):
        pm.write_int(self.FOVChanger, self.FOV)

    def toogle_spotted(self):
        self.aimbot.toogle_spotted()

    def toogle_autostrafe(self):
        self.mainthread.toogle_autostrafe()

    def toogle_bhop(self):
        self.mainthread.toogle_bunnyhop()

    def fov_slider_set_value(self, val):
        val = float(val) * 10
        val = int(val)
        if 0.1 < val < 360:
            self.mainwindow_ui.fovSlider.setValue(val)

    def update_aimbot_fov(self):
        fov = self.mainwindow_ui.fovSlider.value() / 10
        self.mainwindow_ui.fovLineEdit.setText(f"{fov}")
        self.aimbot.update_fov(fov)

    def update_aimbot_aimspot(self):
        if self.mainwindow_ui.aimspotBox.currentText() == "Body":
            self.aimbot.update_aimspot(5)
        if self.mainwindow_ui.aimspotBox.currentText() == "Head":
            self.aimbot.update_aimspot(8)

    def toogle_glow(self):
        self.mainthread.toogle_glow()

    def start_aimbot(self):
        self.aimbot.toogle_enabled()

        # if self.aimbot_enabled:
        #     self.aimbot_enabled = False
        #     self.aimbot.terminate()
        # else:
        #     self.aimbot_enabled = True
        #     self.aimbot.start()

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


def run():
    global pm
    global client
    global engine
    global engine_pointer
    global Local_Player
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    cvars = pymem.process.module_from_name(pm.process_handle, 'vstdlib.dll').lpBaseOfDll
    engine_pointer = pm.read_uint(engine + dwClientState)
    Local_Player = pm.read_uint(client + dwLocalPlayer)
    modules = list(pm.list_modules())
    for module in modules:
        if module.name == 'vstdlib.dll':
            print(pymem.pattern.pattern_scan_module(pm.process_handle, module, b'sv_cheats'))

    # pymem.pattern.pattern_scan_module(pm, cvars, b'sv_cheats')

    # print(pm.read_string(cvars + ))
    # pymem.pattern.scan_pattern_page(pm, )

    app = QApplication(["matplotlib"])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
