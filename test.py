import platform
import math
from ctypes import *
from classes.Classes import *

ntdll = windll.ntdll
k32 = windll.kernel32
mem = Process('csgo.exe')
vt = InterfaceList()
nv = NetVarList()

glow_pointer = mem.read_i32(nv.dwGlowObjectManager)
while True:
    if Engine.is_in_game():
        self = Entity.get_client_entity(Engine.get_local_player())
        view_angle = Engine.get_view_angles()
        glow_pointer = mem.read_i32(nv.dwGlowObjectManager)
        for i in range(0, Engine.get_max_clients()):
            entity = Entity.get_client_entity(i)
            if not entity.is_valid():
                continue
            if self.get_team_num() == entity.get_team_num():
                continue
            entity_health = entity.get_health() / 100.0
            index = mem.read_i32(entity.address + nv.m_iGlowIndex) * 0x38
            mem.write_float(glow_pointer + index + 0x08, 1.0 - entity_health)  # r
            mem.write_float(glow_pointer + index + 0x0C, entity_health)  # g
            mem.write_float(glow_pointer + index + 0x10, 0.0)  # b
            mem.write_float(glow_pointer + index + 0x14, 0.8)  # a
            mem.write_i8(glow_pointer + index + 0x28, 1)
            mem.write_i8(glow_pointer + index + 0x29, 0)
