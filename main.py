from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from global_hotkeys import *
import pymem
from settings.mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer, TargetPlayer
from offsets.offsets import *
from keyboard import is_pressed
from funcs.bunnyhop import Bhop, AutoStrafe
import win32gui


class WindowThread(QThread):
    update_progress = pyqtSignal(str)

    def send_signal(self):
        self.update_progress.emit("press")

    def run(self):
        binding = [[["insert"], None, self.send_signal], [["insert"], None, self.send_signal],
                   [["insert"], None, self.send_signal]]
        register_hotkeys(binding)
        start_checking_hotkeys()


class BunnyhopThread(QThread):
    def __init__(self):
        super().__init__()
        self.Autostrafe = False
        self.OldViewangle = 0

    def toogle_autostrafe(self):
        if self.Autostrafe:
            self.Autostrafe = False
        else:
            self.Autostrafe = True

    def run(self):
        while True:
            if is_pressed("space"):
                Bhop(pm, client, Local_Player)

            if self.Autostrafe:  # Autostrafe
                y_angle = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                y_angle = AutoStrafe(pm, client, Local_Player, y_angle, self.OldViewangle)
                self.OldViewangle = y_angle


class GlowThread(QThread):
    def run(self):
        while True:
            glow(pm, client)


class AimbotThread(QThread):
    update_localpos = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.FOV = 1
        self.Aimspot = 8
        self.Spotted = False
        self.Silent = False
        self.RCS = False
        self.Rage = False

    def update_fov(self, fov):
        self.FOV = fov

    def update_aimspot(self, aimspot):
        self.Aimspot = aimspot

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
        else:
            self.RCS = True

    def toogle_rage(self):
        if self.Rage:
            self.Rage = False
        else:
            self.Rage = True

    def run(self):
        local_player = LocalPlayer(pm, client, engine_pointer, engine)
        local_player.get()
        while True:
            old_distance_x = 111111111
            old_distance_y = 111111111

            for i in range(32):
                target_player = pm.read_uint(client + dwEntityList + i * 0x10)
                target_player = TargetPlayer(target_player, self.Aimspot, pm)

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
                    old_distance_x, old_distance_y = local_player.aim_at(target_player, old_distance_x, old_distance_y,
                                                                         self.Spotted, self.FOV, self.Silent, self.RCS)
                except TypeError:
                    continue


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

        self.glow = GlowThread()
        self.glow_enabled = False

        self.aimbot = AimbotThread()
        self.aimbot_enabled = False

        self.bunnyhop = BunnyhopThread()
        self.bunnyhop_enabled = False

        # Aimbot
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.fovLineEdit.textChanged.connect(self.fov_slider_set_value)
        self.mainwindow_ui.aimspotBox.activated.connect(self.update_aimbot_aimspot)
        self.mainwindow_ui.silentaimCheckBox.stateChanged.connect(self.toogle_silentaim)
        self.mainwindow_ui.spottedCheckBox.stateChanged.connect(self.toogle_spotted)
        self.mainwindow_ui.rcsCheckBox.stateChanged.connect(self.toogle_rcs)
        self.mainwindow_ui.rageCheckBox.stateChanged.connect(self.toogle_rage)

        # Visuals
        self.mainwindow_ui.enableglowCheckBox.stateChanged.connect(self.start_glow)
        self.mainwindow_ui.fovchangerSlider.valueChanged.connect(self.fov_changer)

        # Misc
        self.mainwindow_ui.enablebunnyhopCheckBox.stateChanged.connect(self.start_bhop)
        self.mainwindow_ui.enableautostrafeCheckBox.stateChanged.connect(self.toogle_autostrafe)

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
        self.bunnyhop.toogle_autostrafe()

    def start_bhop(self):
        if self.bunnyhop_enabled:
            self.bunnyhop_enabled = False
            self.bunnyhop.terminate()
        else:
            self.bunnyhop_enabled = True
            self.bunnyhop.start()

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

    def start_glow(self):
        if self.glow_enabled:
            self.glow_enabled = False
            self.glow.terminate()
        else:
            self.glow_enabled = True
            self.glow.start()

    def start_aimbot(self):
        if self.aimbot_enabled:
            self.aimbot_enabled = False
            self.aimbot.terminate()
        else:
            self.aimbot_enabled = True
            self.aimbot.start()

    def open_close(self):
        if self.mainwindow_ui.tabWidget.isHidden():
            self.mainwindow_ui.tabWidget.show()
            self.mainwindow_ui.frame.show()
        else:
            self.mainwindow_ui.tabWidget.hide()
            self.mainwindow_ui.frame.hide()

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
    engine_pointer = pm.read_uint(engine + dwClientState)
    Local_Player = pm.read_uint(client + dwLocalPlayer)

    app = QApplication(["matplotlib"])
    mainwindow = MainWindow()
    ID = mainwindow.winId()
    win32gui.SetForegroundWindow(ID)
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
