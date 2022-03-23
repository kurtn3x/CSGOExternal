from ctypes import *
k32 = windll.kernel32
ntdll = windll.ntdll


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


class NetVarTable:
    def __init__(self, name, mem,vt):
        self.table = 0
        self.mem = mem
        self.vt = vt
        a0 = self.mem.read_i32(self.mem.read_i32(self.vt.client.function(8) + 1))
        while a0 != 0:
            a1 = self.mem.read_i32(a0 + 0x0C)
            if name.encode('ascii', 'ignore') == self.mem.read_string(self.mem.read_i32(a1 + 0x0C), 120):
                self.table = a1
                return
            a0 = self.mem.read_i32(a0 + 0x10)
        raise Exception("NetVarTable [" + name + "] not found!")

    def get_offset(self, name):
        offset = self.__get_offset(self.table, name)
        if offset == 0:
            raise Exception("Offset [" + name + "] not found!")
        return offset

    def __get_offset(self, address, name):
        a0 = 0
        for a1 in range(0, self.mem.read_i32(address + 0x4)):
            a2 = a1 * 60 + self.mem.read_i32(address)
            a3 = self.mem.read_i32(a2 + 0x2C)
            a4 = self.mem.read_i32(a2 + 0x28)
            if a4 != 0 and self.mem.read_i32(a4 + 0x4) != 0:
                a5 = self.__get_offset(a4, name)
                if a5 != 0:
                    a0 += a3 + a5
            if name.encode('ascii', 'ignore') == self.mem.read_string(self.mem.read_i32(a2), 120):
                return a3 + a0
        return a0


class VirtualTable:
    def __init__(self, table, mem):
        self.table = table
        self.mem = mem

    def function(self, index):
        return self.mem.read_i32(self.mem.read_i32(self.table) + index * 4)


class Player:
    def __init__(self, address, mem, nv):
        self.address = address
        self.mem = mem
        self.nv = nv

    def get_team_num(self):
        return self.mem.read_i32(self.address + self.nv.m_iTeamNum)

    def get_health(self):
        return self.mem.read_i32(self.address + self.nv.m_iHealth)

    def get_life_state(self):
        return self.mem.read_i32(self.address + self.nv.m_lifeState)

    def get_tick_count(self):
        return self.mem.read_i32(self.address + self.nv.m_nTickBase)

    def get_shots_fired(self):
        return self.mem.read_i32(self.address + self.nv.m_iShotsFired)

    def get_cross_index(self):
        return self.mem.read_i32(self.address + self.nv.m_iCrossHairID)

    def get_weapon(self):
        a0 = self.mem.read_i32(self.address + self.nv.m_hActiveWeapon)
        return self.mem.read_i32(self.nv.dwEntityList + ((a0 & 0xFFF) - 1) * 0x10)

    def get_weapon_id(self):
        return self.mem.read_i32(self.get_weapon() + self.nv.m_iItemDefinitionIndex)

    def get_origin(self):
        return self.mem.read_vec3(self.address + self.nv.m_vecOrigin)

    def get_vec_view(self):
        return self.mem.read_vec3(self.address + self.nv.m_vecViewOffset)

    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_origin()
        return Vector3(v.x + o.x, v.y + o.y, v.z + o.z)

    def get_vec_punch(self):
        return self.mem.read_vec3(self.address + self.nv.m_vecPunch)

    def get_bone_pos(self, index):
        a0 = 0x30 * index
        a1 = self.mem.read_i32(self.address + self.nv.m_dwBoneMatrix)
        return Vector3(
            self.mem.read_float(a1 + a0 + 0x0C),
            self.mem.read_float(a1 + a0 + 0x1C),
            self.mem.read_float(a1 + a0 + 0x2C)
        )

    def is_valid(self):
        health = self.get_health()
        return self.address != 0 and self.get_life_state() == 0 and 0 < health < 1338


class Engine:
    @staticmethod
    def get_local_player(mem, nv):
        return mem.read_i32(nv.dwClientState + nv.dwGetLocalPlayer)

    @staticmethod
    def get_view_angles(mem, nv):
        return mem.read_vec3(nv.dwClientState + nv.dwViewAngles)

    @staticmethod
    def get_max_clients(mem, nv):
        return mem.read_i32(nv.dwClientState + nv.dwMaxClients)

    @staticmethod
    def is_in_game(mem, nv):
        return mem.read_i8(nv.dwClientState + nv.dwState) >> 2


class Entity:
    @staticmethod
    def get_client_entity(index, mem, nv):
        return Player(mem.read_i32(nv.dwEntityList + index * 0x10), mem, nv)


class InterfaceTable:
    def __init__(self, name, mem):
        self.mem = mem
        self.table_list = self.mem.read_i32(self.mem.read_i32(self.mem.get_export(self.mem.get_module(name), 'CreateInterface') - 0x6A))

    def get_interface(self, name):
        a0 = self.table_list
        while a0 != 0:
            if name.encode('ascii', 'ignore') == self.mem.read_string(self.mem.read_i32(a0 + 0x4), 120)[0:-3]:
                return VirtualTable(self.mem.read_i32(self.mem.read_i32(a0) + 1), self.mem)
            a0 = self.mem.read_i32(a0 + 0x8)
        raise Exception("Interface [" + name + "] not found!")


class InterfaceList:
    def __init__(self, mem):
        self.mem = mem
        table = InterfaceTable('client.dll', self.mem)
        self.client = table.get_interface('VClient')
        self.entity = table.get_interface('VClientEntityList')
        table = InterfaceTable('engine.dll', self.mem)
        self.engine = table.get_interface('VEngineClient')
        table = InterfaceTable('vstdlib.dll', self.mem)
        self.cvar = table.get_interface('VEngineCvar')
        table = InterfaceTable('inputsystem.dll', self.mem)
        self.input = table.get_interface('InputSystemVersion')


class NetVarList:
    def __init__(self, mem, vt):
        table = NetVarTable('DT_BasePlayer', mem, vt)
        self.m_iHealth = table.get_offset('m_iHealth')
        self.m_vecViewOffset = table.get_offset('m_vecViewOffset[0]')
        self.m_lifeState = table.get_offset('m_lifeState')
        self.m_nTickBase = table.get_offset('m_nTickBase')
        self.m_vecPunch = table.get_offset('m_Local') + 0x70

        table = NetVarTable('DT_BaseEntity', mem, vt)
        self.m_iTeamNum = table.get_offset('m_iTeamNum')
        self.m_vecOrigin = table.get_offset('m_vecOrigin')

        table = NetVarTable('DT_CSPlayer', mem, vt)
        self.m_hActiveWeapon = table.get_offset('m_hActiveWeapon')
        self.m_iShotsFired = table.get_offset('m_iShotsFired')
        self.m_iCrossHairID = table.get_offset('m_bHasDefuser') + 0x5C
        self.m_iGlowIndex = table.get_offset('m_flFlashDuration') + 0x18

        table = NetVarTable('DT_BaseAnimating', mem, vt)
        self.m_dwBoneMatrix = table.get_offset('m_nForceBone') + 0x1C

        table = NetVarTable('DT_BaseAttributableItem', mem, vt)
        self.m_iItemDefinitionIndex = table.get_offset('m_iItemDefinitionIndex')

        self.dwEntityList = vt.entity.table - (mem.read_i32(vt.entity.function(6) + 0x22) - 0x38)
        self.dwClientState = mem.read_i32(mem.read_i32(vt.engine.function(18) + 0x21))
        self.dwGetLocalPlayer = mem.read_i32(vt.engine.function(12) + 0x16)
        self.dwViewAngles = mem.read_i32(vt.engine.function(19) + 0x191)
        self.dwMaxClients = mem.read_i32(vt.engine.function(20) + 0x07)
        self.dwState = mem.read_i32(vt.engine.function(26) + 0x07)
        self.dwButton = mem.read_i32(vt.input.function(28) + 0xC1 + 2)
        self.dwGlowObjectManager = mem.find_pattern("client.dll", b'\xA1\x00\x00\x00\x00\xA8\x01\x75\x4B', "x????xxxx")