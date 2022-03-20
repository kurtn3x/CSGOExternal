from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from global_hotkeys import *
import time
import pymem
from mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer, TargetPlayer
from classes.Vector import Vector

# write offset parser
m_iHealth = 0x100
dwEntityList = 0x4DCEEAC
dwLocalPlayer = 0xDB35DC
dwGlowObjectManager = 0x5317308
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4
dwClientState = 0x58CFC4
dwClientState_ViewAngles = 0x4D90
m_bDormant = 0xED
m_vecOrigin = 0x138
m_vecViewOffset = 0x108
m_dwBoneMatrix = 0x26A8
clientstate_net_channel = 0x9C
clientstate_last_outgoing_command = 0x4D2C
dwClientState_MaxPlayer = 0x388


class WindowThread(QThread):
    update_progress = pyqtSignal(str)

    def send_signal(self):
        self.update_progress.emit("press")

    def run(self):
        binding = [[["insert"], None, self.send_signal], [["insert"], None, self.send_signal],
                   [["insert"], None, self.send_signal]]
        register_hotkeys(binding)
        start_checking_hotkeys()


class GlowThread(QThread):
    def run(self):
        glow(pm, client, dwGlowObjectManager, dwEntityList, m_iTeamNum, m_iGlowIndex)


class AimbotThread(QThread):
    update_localpos = pyqtSignal(tuple)
    update_targetpos = pyqtSignal(tuple)
    update_targetpos2 = pyqtSignal(tuple)
    update_viewangles = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.FOV = 90
        self.AIMSPOT = 8
        self.running = True

    def update_fov(self, fov):
        self.FOV = fov

    def update_aimspot(self, aimspot):
        self.AIMSPOT = aimspot

    def run(self):
        while True:
            print(self.AIMSPOT)
            time.sleep(0.000001)
            OldDelta = Vector(0, 0, 0)
            local_player = LocalPlayer(pm, client, engine_pointer)
            view_angle_x = pm.read_float(engine_pointer + dwClientState_ViewAngles)
            view_angle_y = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
            self.update_viewangles.emit((view_angle_x, view_angle_y))
            local_player.get()
            local_player.get_view_offset()
            local_player.get_origin()
            self.update_localpos.emit((local_player.Origin.x, local_player.Origin.y, local_player.Origin.z))
            closestDistance = 1000000
            closestDistanceIndex = -1
            for i in range(32):
                target_player = TargetPlayer(i, pm, client, self.AIMSPOT)
                if target_player.TargetPlayer:
                    target_player.get_origin()
                    target_player.get_team()
                    target_player.get_view_offset()
                    target_player.get_health()
                    target_player.get_bone_matrix()
                    local_player.get_team()
                    local_player.get_health()
                    if target_player.Team == local_player.Team:
                        continue
                    if target_player.Health < 1 or local_player.Health < 1:
                        continue
                    if not local_player.LocalPlayer:
                        continue
                    if local_player.LocalPlayer == target_player.TargetPlayer:
                        continue

                    currentDistance = local_player.get_distance(target_player.Origin)
                    if currentDistance < closestDistance:
                        closestDistance = currentDistance
                        closestEnemy = target_player
                        closestDistanceIndex = i
            if closestDistanceIndex == -1:
                pass
            else:
                self.update_targetpos.emit((closestEnemy.BonePos.x, closestEnemy.BonePos.y, closestEnemy.BonePos.z))
                OldDelta = local_player.aim_at(closestEnemy.BonePos, OldDelta, self.FOV)
                self.update_targetpos2.emit((local_player.Pitch, local_player.Yaw, "cock"))


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

        self.mainwindow_ui.glowButton.clicked.connect(self.start_glow)
        self.glow = GlowThread()
        self.glow_enabled = False
        self.aimbot_enabled = False

        self.mainwindow_ui.LocalPlayer1.setText("Local Player")
        self.mainwindow_ui.TargetPlayer1.setText("Target Head")
        self.mainwindow_ui.TargetPlayer5.setText("Calculated Pitch, Yaw")
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.aimspotBox.activated.connect(self.update_aimbot_aimspot)
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)

    def update_aimbot_fov(self):
        self.aimbot.update_fov(self.mainwindow_ui.fovSlider.value())

    def update_aimbot_aimspot(self):
        if self.mainwindow_ui.aimspotBox.currentText() == "Body":
            self.aimbot.update_aimspot(5)
        if self.mainwindow_ui.aimspotBox.currentText() == "Head":
            self.aimbot.update_aimspot(8)

    def update_viewangles(self, val):
        x = val[0]
        y = val[1]
        self.mainwindow_ui.ViewAngle1.setText(f"Current Pitch: {x}")
        self.mainwindow_ui.ViewAngle2.setText(f"Current Yaw: {y}")

    def update_localpos(self, val):
        x = val[0]
        y = val[1]
        z = val[2]
        self.mainwindow_ui.LocalPlayer2.setText(f"X {x}")
        self.mainwindow_ui.LocalPlayer3.setText(f"Y {y}")
        self.mainwindow_ui.LocalPlayer4.setText(f"Z {z}")

    def update_targetpos(self, val):
        x = val[0]
        y = val[1]
        z = val[2]
        self.mainwindow_ui.TargetPlayer2.setText(f"X {x}")
        self.mainwindow_ui.TargetPlayer3.setText(f"Y {y}")
        self.mainwindow_ui.TargetPlayer4.setText(f"Z {z}")

    def update_targetpos2(self, val):
        x = val[0]
        y = val[1]
        z = val[2]
        self.mainwindow_ui.TargetPlayer6.setText(f"Pitch {x}")
        self.mainwindow_ui.TargetPlayer7.setText(f"Yaw {y}")

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
            self.aimbot = AimbotThread()
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
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


def run():
    global pm
    global client
    global engine
    global engine_pointer
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    engine_pointer = pm.read_uint(engine + dwClientState)

    app = QApplication(["matplotlib"])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
