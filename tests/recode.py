import platform
import math
from ctypes import *
from PyQt5.QtWidgets import *
import sys
from settings.mainwindow import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from math import *
from funcs.aimbot import normalizeAngles, calc_distance
from ctypes import c_uint32, pointer


ntdll = windll.ntdll
k32 = windll.kernel32
u32 = windll.user32
#
# ekknod@2019
#


g_glow = True
g_rcs = True
g_aimbot = True
g_aimbot_rcs = True
g_aimbot_head = True
g_aimbot_fov = 180
g_aimbot_smooth = 0
g_aimbot_key = 107
g_triggerbot_key = 111
g_exit_key = 72

g_old_punch = 0
g_previous_tick = 0
g_current_tick = 0


class Vector3(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]


class PROCESSENTRY32(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("cntUsage", c_uint32),
        ("th32ProcessID", c_uint32),
        ("th32DefaultHeapID", c_uint64),
        ("th32ModuleID", c_uint32),
        ("cntThreads", c_uint32),
        ("th32ParentProcessID", c_uint32),
        ("pcPriClassBase", c_uint32),
        ("dwFlags", c_uint32),
        ("szExeFile", c_char * 260)
    ]


class Process:
    @staticmethod
    def get_process_handle(name):
        handle = 0
        entry = PROCESSENTRY32()
        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)
        entry.dwSize = sizeof(PROCESSENTRY32)
        while k32.Process32Next(snap, pointer(entry)):
            if entry.szExeFile == name.encode("ascii", "ignore"):
                handle = k32.OpenProcess(0x430, 0, entry.th32ProcessID)
                break
        k32.CloseHandle(snap)
        return handle

    @staticmethod
    def get_process_peb(handle, wow64):
        buffer = (c_uint64 * 6)(0)
        if wow64:
            if ntdll.NtQueryInformationProcess(handle, 26, pointer(buffer), 8, 0) == 0:
                return buffer[0]
        else:
            if ntdll.NtQueryInformationProcess(handle, 0, pointer(buffer), 48, 0) == 0:
                return buffer[1]
        return 0

    def __init__(self, name):
        self.mem = self.get_process_handle(name)
        if self.mem == 0:
            raise Exception("Process [" + name + "] not found!")
        self.peb = self.get_process_peb(self.mem, True)
        if self.peb == 0:
            self.peb = self.get_process_peb(self.mem, False)
            self.wow64 = False
        else:
            self.wow64 = True

    def is_running(self):
        buffer = c_uint32()
        k32.GetExitCodeProcess(self.mem, pointer(buffer))
        return buffer.value == 0x103

    def read_vec3(self, address):
        buffer = Vector3()
        ntdll.NtReadVirtualMemory(self.mem, c_long(address), pointer(buffer), 12, 0)
        return buffer

    def read_buffer(self, address, length):
        buffer = (c_uint8 * length)()
        ntdll.NtReadVirtualMemory(self.mem, address, buffer, length, 0)
        return buffer

    def read_string(self, address, length=120):
        buffer = create_string_buffer(length)
        ntdll.NtReadVirtualMemory(self.mem, address, buffer, length, 0)
        return buffer.value

    def read_unicode(self, address, length=120):
        buffer = create_unicode_buffer(length)
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_float(self, address, length=4):
        buffer = c_float()
        ntdll.NtReadVirtualMemory(self.mem, c_long(address), pointer(buffer), length, 0)
        return buffer.value

    def read_i8(self, address, length=1):
        buffer = c_uint8()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i16(self, address, length=2):
        buffer = c_uint16()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i32(self, address, length=4):
        buffer = c_uint32()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i64(self, address, length=8):
        buffer = c_uint64()
        ntdll.NtReadVirtualMemory(self.mem, c_uint64(address), pointer(buffer), length, 0)
        return buffer.value

    def write_float(self, address, value):
        buffer = c_float(value)
        return ntdll.NtWriteVirtualMemory(self.mem, address, pointer(buffer), 4, 0) == 0

    def write_i8(self, address, value):
        buffer = c_uint8(value)
        return ntdll.NtWriteVirtualMemory(self.mem, address, pointer(buffer), 1, 0) == 0

    def write_i16(self, address, value):
        buffer = c_uint16(value)
        return ntdll.NtWriteVirtualMemory(self.mem, address, pointer(buffer), 2, 0) == 0

    def write_i64(self, address, value):
        buffer = c_uint64(value)
        return ntdll.NtWriteVirtualMemory(self.mem, address, pointer(buffer), 8, 0) == 0

    def get_module(self, name):
        if self.wow64:
            a0 = [0x04, 0x0C, 0x14, 0x28, 0x10]
        else:
            a0 = [0x08, 0x18, 0x20, 0x50, 0x20]
        a1 = self.read_i64(self.read_i64(self.peb + a0[1], a0[0]) + a0[2], a0[0])
        a2 = self.read_i64(a1 + a0[0], a0[0])
        while a1 != a2:
            val = self.read_unicode(self.read_i64(a1 + a0[3], a0[0]))
            if str(val).lower() == name.lower():
                return self.read_i64(a1 + a0[4], a0[0])
            a1 = self.read_i64(a1, a0[0])
        raise Exception("Module [" + name + "] not found!")

    def get_export(self, module, name):
        if module == 0:
            return 0
        a0 = self.read_i32(module + self.read_i16(module + 0x3C) + (0x88 - self.wow64 * 0x10)) + module
        a1 = [self.read_i32(a0 + 0x18), self.read_i32(a0 + 0x1c), self.read_i32(a0 + 0x20), self.read_i32(a0 + 0x24)]
        while a1[0] > 0:
            a1[0] -= 1
            export_name = self.read_string(module + self.read_i32(module + a1[2] + (a1[0] * 4)), 120)
            if name.encode('ascii', 'ignore') == export_name:
                a2 = self.read_i16(module + a1[3] + (a1[0] * 2))
                a3 = self.read_i32(module + a1[1] + (a2 * 4))
                return module + a3
        raise Exception("Export [" + name + "] not found!")

    def find_pattern(self, module_name, pattern, mask):
        a0 = self.get_module(module_name)
        a1 = self.read_i32(a0 + 0x03C) + a0
        a2 = self.read_i32(a1 + 0x01C)
        a3 = self.read_i32(a1 + 0x02C)
        a4 = self.read_buffer(a0 + a3, a2)
        for a5 in range(0, a2):
            a6 = 0
            for a7 in range(0, pattern.__len__()):
                if mask[a7] == 'x' and a4[a5 + a7] != pattern[a7]:
                    break
                a6 = a6 + 1
            if a6 == pattern.__len__():
                return a0 + a3 + a5
        return 0


class VirtualTable:
    def __init__(self, table):
        self.table = table

    def function(self, index):
        return mem.read_i32(mem.read_i32(self.table) + index * 4)


class InterfaceTable:
    def __init__(self, name):
        self.table_list = mem.read_i32(mem.read_i32(mem.get_export(mem.get_module(name), 'CreateInterface') - 0x6A))

    def get_interface(self, name):
        a0 = self.table_list
        while a0 != 0:
            if name.encode('ascii', 'ignore') == mem.read_string(mem.read_i32(a0 + 0x4), 120)[0:-3]:
                return VirtualTable(mem.read_i32(mem.read_i32(a0) + 1))
            a0 = mem.read_i32(a0 + 0x8)
        raise Exception("Interface [" + name + "] not found!")


class NetVarTable:
    def __init__(self, name):
        self.table = 0
        a0 = mem.read_i32(mem.read_i32(vt.client.function(8) + 1))
        while a0 != 0:
            a1 = mem.read_i32(a0 + 0x0C)
            if name.encode('ascii', 'ignore') == mem.read_string(mem.read_i32(a1 + 0x0C), 120):
                self.table = a1
                return
            a0 = mem.read_i32(a0 + 0x10)
        raise Exception("NetVarTable [" + name + "] not found!")

    def get_offset(self, name):
        offset = self.__get_offset(self.table, name)
        if offset == 0:
            raise Exception("Offset [" + name + "] not found!")
        return offset

    def __get_offset(self, address, name):
        a0 = 0
        for a1 in range(0, mem.read_i32(address + 0x4)):
            a2 = a1 * 60 + mem.read_i32(address)
            a3 = mem.read_i32(a2 + 0x2C)
            a4 = mem.read_i32(a2 + 0x28)
            if a4 != 0 and mem.read_i32(a4 + 0x4) != 0:
                a5 = self.__get_offset(a4, name)
                if a5 != 0:
                    a0 += a3 + a5
            if name.encode('ascii', 'ignore') == mem.read_string(mem.read_i32(a2), 120):
                return a3 + a0
        return a0


class ConVar:
    def __init__(self, name):
        self.address = 0
        a0 = mem.read_i32(mem.read_i32(mem.read_i32(vt.cvar.table + 0x34)) + 0x4)
        while a0 != 0:
            if name.encode('ascii', 'ignore') == mem.read_string(mem.read_i32(a0 + 0x0C)):
                self.address = a0
                return
            a0 = mem.read_i32(a0 + 0x4)
        raise Exception("ConVar [" + name + "] not found!")

    def get_int(self):
        a0 = c_int32()
        a1 = mem.read_i32(self.address + 0x30) ^ self.address
        ntdll.memcpy(pointer(a0), pointer(c_int32(a1)), 4)
        return a0.value

    def get_float(self):
        a0 = c_float()
        a1 = mem.read_i32(self.address + 0x2C) ^ self.address
        ntdll.memcpy(pointer(a0), pointer(c_int32(a1)), 4)
        return a0.value


class InterfaceList:
    def __init__(self):
        table = InterfaceTable('client.dll')
        self.client = table.get_interface('VClient')
        self.entity = table.get_interface('VClientEntityList')
        table = InterfaceTable('engine.dll')
        self.engine = table.get_interface('VEngineClient')
        table = InterfaceTable('vstdlib.dll')
        self.cvar = table.get_interface('VEngineCvar')
        table = InterfaceTable('inputsystem.dll')
        self.input = table.get_interface('InputSystemVersion')


class NetVarList:
    def __init__(self):
        table = NetVarTable('DT_BasePlayer')
        self.m_iHealth = table.get_offset('m_iHealth')
        self.m_vecViewOffset = table.get_offset('m_vecViewOffset[0]')
        self.m_lifeState = table.get_offset('m_lifeState')
        self.m_nTickBase = table.get_offset('m_nTickBase')
        self.m_vecPunch = table.get_offset('m_Local') + 0x70

        table = NetVarTable('DT_BaseEntity')
        self.m_iTeamNum = table.get_offset('m_iTeamNum')
        self.m_vecOrigin = table.get_offset('m_vecOrigin')

        table = NetVarTable('DT_CSPlayer')
        self.m_hActiveWeapon = table.get_offset('m_hActiveWeapon')
        self.m_iShotsFired = table.get_offset('m_iShotsFired')
        self.m_iCrossHairID = table.get_offset('m_bHasDefuser') + 0x5C
        self.m_iGlowIndex = table.get_offset('m_flFlashDuration') + 0x18
        self.m_iFOV = table.get_offset('m_iFOV')

        table = NetVarTable('DT_BaseAnimating')
        self.m_dwBoneMatrix = table.get_offset('m_nForceBone') + 0x1C

        table = NetVarTable('DT_BaseAttributableItem')
        self.m_iItemDefinitionIndex = table.get_offset('m_iItemDefinitionIndex')

        self.dwEntityList = vt.entity.table - (mem.read_i32(vt.entity.function(6) + 0x22) - 0x38)
        # self.dwEntityList = mem.find_pattern("client.dll", b'\xBB\x00\x00\x00\x00\x83\xFF\x01\x0F\x8C\x00\x00\x00\x00\x3B\xF8')
        self.dwClientState = mem.read_i32(mem.read_i32(vt.engine.function(18) + 0x21))
        self.dwGetLocalPlayer = mem.read_i32(vt.engine.function(12) + 0x16)
        self.dwViewAngles = mem.read_i32(vt.engine.function(19) + 0x191)
        self.dwMaxClients = mem.read_i32(vt.engine.function(20) + 0x07)
        self.dwState = mem.read_i32(vt.engine.function(26) + 0x07)
        self.dwButton = mem.read_i32(vt.input.function(28) + 0xC1 + 2)
        self.dwGlowObjectManager = mem.find_pattern("client.dll", b'\xA1\x00\x00\x00\x00\xA8\x01\x75\x4B', "x????xxxx")
        self.dwGlowObjectManager = mem.read_i32(self.dwGlowObjectManager + 1) + 4


class Player:
    def __init__(self, address):
        self.address = address

    def get_team_num(self):
        return mem.read_i32(self.address + nv.m_iTeamNum)

    def get_health(self):
        return mem.read_i32(self.address + nv.m_iHealth)

    def get_life_state(self):
        return mem.read_i32(self.address + nv.m_lifeState)

    def get_tick_count(self):
        return mem.read_i32(self.address + nv.m_nTickBase)

    def get_shots_fired(self):
        return mem.read_i32(self.address + nv.m_iShotsFired)

    def get_cross_index(self):
        return mem.read_i32(self.address + nv.m_iCrossHairID)

    def get_weapon(self):
        a0 = mem.read_i32(self.address + nv.m_hActiveWeapon)
        return mem.read_i32(nv.dwEntityList + ((a0 & 0xFFF) - 1) * 0x10)

    def get_weapon_id(self):
        return mem.read_i32(self.get_weapon() + nv.m_iItemDefinitionIndex)

    def get_origin(self):
        return mem.read_vec3(self.address + nv.m_vecOrigin)

    def get_vec_view(self):
        return mem.read_vec3(self.address + nv.m_vecViewOffset)

    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_origin()
        return Vector3(v.x + o.x, v.y + o.y, v.z + o.z)

    def get_vec_punch(self):
        return mem.read_vec3(self.address + nv.m_vecPunch)

    def get_bone_pos(self, index):
        a0 = 0x30 * index
        a1 = mem.read_i32(self.address + nv.m_dwBoneMatrix)
        return Vector3(
            mem.read_float(a1 + a0 + 0x0C),
            mem.read_float(a1 + a0 + 0x1C),
            mem.read_float(a1 + a0 + 0x2C)
        )

    def is_valid(self):
        health = self.get_health()
        return self.address != 0 and self.get_life_state() == 0 and 0 < health < 1338


class Engine:
    @staticmethod
    def get_local_player():
        return mem.read_i32(nv.dwClientState + nv.dwGetLocalPlayer)

    @staticmethod
    def get_view_angles():
        return mem.read_vec3(nv.dwClientState + nv.dwViewAngles)

    @staticmethod
    def get_max_clients():
        return mem.read_i32(nv.dwClientState + nv.dwMaxClients)

    @staticmethod
    def is_in_game():
        return mem.read_i8(nv.dwClientState + nv.dwState) >> 2


class Entity:
    @staticmethod
    def get_client_entity(index):
        return Player(mem.read_i32(nv.dwEntityList + index * 0x10))

aimbot = True
# Local_Player = pm.read_uint(client + dwLocalPlayer)
class Thread(QThread):
    def run(self):
        while True:
            while mem.is_running():
                k32.Sleep(1)
                if Engine.is_in_game():
                    self = Entity.get_client_entity(Engine.get_local_player())
                    mem.write_i16(Engine.get_local_player() + nv.m_iFOV, 60)
                    fl_sensitivity = _sensitivity.get_float()
                    view_angle = Engine.get_view_angles()
                    if g_glow:
                        glow_pointer = mem.read_i32(nv.dwGlowObjectManager)
                        for i in range(0, Engine.get_max_clients()):
                            entity = Entity.get_client_entity(i)
                            if not entity.is_valid():
                                continue
                            if not mp_teammates_are_enemies.get_int() and self.get_team_num() == entity.get_team_num():
                                continue
                            entity_health = entity.get_health() / 100.0
                            index = mem.read_i32(entity.address + nv.m_iGlowIndex) * 0x38
                            mem.write_float(glow_pointer + index + 0x08, 1.0 - entity_health)  # r
                            mem.write_float(glow_pointer + index + 0x0C, entity_health)  # g
                            mem.write_float(glow_pointer + index + 0x10, 0.0)  # b
                            mem.write_float(glow_pointer + index + 0x14, 0.8)  # a
                            mem.write_i8(glow_pointer + index + 0x28, 1)
                            mem.write_i8(glow_pointer + index + 0x29, 0)
                    if aimbot:
                        old_distance_x = 111111111
                        old_distance_y = 111111111
                        for i in range(0, Engine.get_max_clients()):
                            entity = Entity.get_client_entity(i)
                            if not entity.is_valid():
                                continue
                            if not mp_teammates_are_enemies.get_int() and self.get_team_num() == entity.get_team_num():
                                continue

                            try:
                                delta = Vector3(0, 0, 0)
                                ent_bone = entity.get_bone_pos(8)
                                loc_org = self.get_origin()
                                viewoffz = self.get_vec_view()
                                viewoffz = viewoffz.z
                                delta.x = loc_org.x - ent_bone.x
                                delta.y = loc_org.y - ent_bone.y
                                delta.z = loc_org.z + viewoffz - ent_bone.z

                                hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
                                pitch = atan(delta.z / hyp) * 180 / pi
                                yaw = atan(delta.y / delta.x) * 180 / pi

                                if delta.x >= 0.0:
                                    yaw += 180.0

                                pitch, yaw = normalizeAngles(pitch, yaw)
                                viewoff = self.get_vec_view()
                                print(pitch, yaw)

                                distance_x, distance_y = calc_distance(viewoff.x, viewoff.y, pitch, yaw)

                                if -89 <= pitch <= 89 and -180 <= yaw <= 180:
                                    if distance_x < g_aimbot_fov and distance_y < g_aimbot_fov:
                                        if distance_x < old_distance_x and distance_y < old_distance_y:
                                            old_distance_x = distance_x
                                            old_distance_y = distance_y
                                            mem.write_float(nv.dwClientState + nv.dwViewAngles, pitch)
                                            mem.write_float(nv.dwClientState + nv.dwViewAngles + 0x4, yaw)
                            except TypeError:
                                continue


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainwindow_ui = Ui_MainWindow()
        self.mainwindow_ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        thread = Thread(parent = self)
        thread.start()


if __name__ == "__main__":

    mem = Process('csgo.exe')
    vt = InterfaceList()
    nv = NetVarList()
    _sensitivity = ConVar('sensitivity')
    mp_teammates_are_enemies = ConVar('mp_teammates_are_enemies')
    app = QApplication(["matplotlib"])
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())



# notes for monkeybrain
# LocalPlayer =
