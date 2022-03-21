from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from global_hotkeys import *
import time
import pymem
from mainwindow import Ui_MainWindow
from funcs.glow import glow
from funcs.aimbot import LocalPlayer, TargetPlayer, normalizeAngles, calc_distance
from classes.Vector import Vector
from math import *
from offsets import *

class WindowThread(QThread):
    update_progress = pyqtSignal(str)

    def send_signal(self):
        self.update_progress.emit("press")

    def run(self):
        binding = [[["insert"], None, self.send_signal], [["insert"], None, self.send_signal],
                   [["insert"], None, self.send_signal]]
        register_hotkeys(binding)
        start_checking_hotkeys()


class VisualsThread(QThread):
    def __init__(self):
        super().__init__()
        self.GlowEnabled = False

    def toogle_glow(self):
        if self.GlowEnabled:
            self.GlowEnabled = False
        else:
            self.GlowEnabled = True

    def run(self):
        while True:
            if self.GlowEnabled:
                glow(pm, client, dwGlowObjectManager, dwEntityList, m_iTeamNum, m_iGlowIndex)


class AimbotThread(QThread):
    update_localpos = pyqtSignal(tuple)
    update_targetpos = pyqtSignal(tuple)
    update_targetpos2 = pyqtSignal(tuple)
    update_viewangles = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.FOV = 1
        self.Aimspot = 8
        self.Spotted = False
        self.Silent = False
        self.RCS = False

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

    def run(self):
        while True:
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
            old_distance_x = 111111111
            old_distance_y = 111111111
            for i in range(32):
                target_player = TargetPlayer(i, pm, client, self.Aimspot)
                if target_player.TargetPlayer:
                    target_player.get_origin()
                    target_player.get_team()
                    target_player.get_view_offset()
                    target_player.get_health()
                    target_player.get_bone_matrix()
                    local_player.get_team()
                    local_player.get_health()
                    target_player.get_dormant()
                    target_player.get_spotted()
                    target_player.get_spotted_mask()
                    local_player.get_id()
                    if target_player.Team == local_player.Team:
                        continue
                    if target_player.Health < 1 or local_player.Health < 1:
                        continue
                    if not local_player.LocalPlayer:
                        continue
                    if local_player.LocalPlayer == target_player.TargetPlayer:
                        continue
                    # if not target_player.Dormant:
                    #     continue

                    delta = Vector(0, 0, 0)
                    delta.x = local_player.Origin.x - target_player.BonePos.x
                    delta.y = local_player.Origin.y - target_player.BonePos.y
                    delta.z = local_player.Origin.z - target_player.BonePos.z
                    hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
                    pitch = atan(delta.z / hyp) * 180 / pi
                    yaw = atan(delta.y / delta.x) * 180 / pi
                    if delta.x >= 0.0:
                        yaw += 180.0

                    pitch, yaw = normalizeAngles(pitch, yaw)
                    if self.Spotted:
                        distance_x, distance_y = calc_distance(local_player.ViewOffset.x, local_player.ViewOffset.y,pitch, yaw)
                        if -89 <= pitch <= 89 and -180 <= yaw <= 180:
                            if distance_x < self.FOV and distance_y < self.FOV:
                                if distance_x < old_distance_x and distance_y < old_distance_y:
                                    old_distance_x = distance_x
                                    old_distance_y = distance_y
                                    if target_player.SpottedMask & (1 << local_player.ID):
                                        if self.Silent & self.RCS: # not working
                                            pm.write_uchar(engine + dwbSendPackets, 0)
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles, pitch)
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
                                            Commands = pm.read_int(client + dwInput + 0xF4)
                                            VerifedCommands = pm.read_int(client + dwInput + 0xF8)
                                            Desired = pm.read_int(engine_pointer + clientstate_last_outgoing_command) + 2
                                            OldUser = Commands + ((Desired - 1) % 150) * 100
                                            VerifedOldUser = VerifedCommands + ((Desired - 1) % 150) * 0x68
                                            m_buttons = pm.read_int(OldUser + 0x30)
                                            Net_Channel = pm.read_uint(engine_pointer + clientstate_net_channel)
                                            if pm.read_int(Net_Channel + 0x18) < Desired:
                                                pass
                                            else:
                                                pm.write_float(OldUser + 0x0C, pitch)
                                                pm.write_float(OldUser + 0x10, yaw)
                                                pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
                                                pm.write_float(VerifedOldUser + 0x0C, pitch)
                                                pm.write_float(VerifedOldUser + 0x10, yaw)
                                                pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
                                                pm.write_uchar(engine + dwbSendPackets, 1)

                                        elif self.Silent and not self.RCS: # not working
                                            pm.write_uchar(engine + dwbSendPackets, 0)
                                            Commands = pm.read_int(client + dwInput + 0xF4)
                                            VerifedCommands = pm.read_int(client + dwInput + 0xF8)
                                            Desired = pm.read_int(engine_pointer + clientstate_last_outgoing_command) + 2
                                            OldUser = Commands + ((Desired - 1) % 150) * 100
                                            VerifedOldUser = VerifedCommands + ((Desired - 1) % 150) * 0x68
                                            # m_buttons = pm.read_int(OldUser + 0x30)
                                            Net_Channel = pm.read_uint(engine_pointer + clientstate_net_channel)
                                            if pm.read_int(Net_Channel + 0x18) < Desired:
                                                print("y")
                                                pm.write_float(OldUser + 0x0C, pitch)
                                                pm.write_float(OldUser + 0x10, yaw)
                                                # pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
                                                pm.write_float(VerifedOldUser + 0x0C, pitch)
                                                pm.write_float(VerifedOldUser + 0x10, yaw)
                                                # pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
                                                pm.write_float(engine_pointer + dwClientState_ViewAngles, pitch)
                                                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
                                                pm.write_uchar(engine + dwbSendPackets, 1)
                                            else:
                                                pm.write_uchar(engine + dwbSendPackets, 1)

                                        elif self.RCS and pm.read_int(local_player.LocalPlayer + m_iShotsFired) > 1:
                                            local_player.get_punch()
                                            print("x")
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles,pitch - (local_player.PunchX * 2))
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, yaw - (local_player.PunchY * 2))

                                        else:
                                            print(pm.read_int(local_player.LocalPlayer + m_iShotsFired))
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles, pitch)
                                            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
                    else:
                        pass
                        # currentDistance = local_player.get_distance(target_player.Origin)
                        # if currentDistance < closestDistance:
                        #     closestDistance = currentDistance
                        #     closestEnemy = target_player
                        #     self.update_targetpos.emit((closestEnemy.BonePos.x, closestEnemy.BonePos.y, closestEnemy.BonePos.z))
                        #     OldDelta = local_player.aim_at(closestEnemy.BonePos, OldDelta, self.FOV, pitch, yaw)
                        #     self.update_targetpos2.emit((local_player.Pitch, local_player.Yaw, "cock"))

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
        self.visuals = VisualsThread()

        self.visuals.start()
        self.aimbot_enabled = False
        self.aimbot = AimbotThread()
        self.aimbot.update_localpos.connect(self.update_localpos)



        # Aimbot
        self.mainwindow_ui.aimbotCheckBox.stateChanged.connect(self.start_aimbot)
        self.mainwindow_ui.fovSlider.valueChanged.connect(self.update_aimbot_fov)
        self.mainwindow_ui.fovLineEdit.textChanged.connect(self.fovSliderSetValue)
        self.mainwindow_ui.aimspotBox.activated.connect(self.update_aimbot_aimspot)
        self.mainwindow_ui.silentaimCheckBox.stateChanged.connect(self.toogle_silentaim)
        self.mainwindow_ui.spottedCheckBox.stateChanged.connect(self.toogle_spotted)
        self.mainwindow_ui.rcsCheckBox.stateChanged.connect(self.toogle_rcs)

        # Visuals
        self.mainwindow_ui.enableglowCheckBox.stateChanged.connect(self.visuals.toogle_glow)

    def toogle_silentaim(self):
        self.aimbot.toogle_silent()

    def toogle_rcs(self):
        self.aimbot.toogle_rcs()

    def toogle_spotted(self):
        self.aimbot.toogle_spotted()

    def fovSliderSetValue(self, val):
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

    def start_glow(self):
        self.visuals.toogle_glow()

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
