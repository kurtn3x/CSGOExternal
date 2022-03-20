import time

from classes.Vector import Vector
from math import *

radian = 57.295779513082
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

class TargetPlayer:
    def __init__(self, index, pm, client, aimspot):
        self.pm = pm
        self.client = client
        self.TargetPlayer = pm.read_uint(client + dwEntityList + index * 0x10)
        self.MaxPlayers = 32
        self.Origin = Vector(0, 0, 0)
        self.Health = 0
        self.Team = 0
        self.BonePos = Vector(0, 0, 0)
        self.ViewOffset = Vector(0, 0, 0)
        if not aimspot or aimspot == "":
            self.Aimspot = 8
        else:
            self.Aimspot = int(aimspot)

    def get_origin(self):
        bone_matrix = self.pm.read_int(self.TargetPlayer + m_dwBoneMatrix)
        self.Origin.x = self.pm.read_float(bone_matrix + 0x30 * 5 + 0x0C)
        self.Origin.y = self.pm.read_float(bone_matrix + 0x30 * 5 + 0x1C)
        self.Origin.z = self.pm.read_float(bone_matrix + 0x30 * 5 + 0x2C)

    def get_health(self):
        self.Health = self.pm.read_int(self.TargetPlayer + m_iHealth)

    def get_team(self):
        self.Team = self.pm.read_int(self.TargetPlayer + m_iTeamNum)

    def get_bone_matrix(self):
        bone_matrix = self.pm.read_int(self.TargetPlayer + m_dwBoneMatrix)
        self.BonePos.x = self.pm.read_float(bone_matrix + 0x30 * self.Aimspot + 0x0C)
        self.BonePos.y = self.pm.read_float(bone_matrix + 0x30 * self.Aimspot + 0x1C)
        self.BonePos.z = self.pm.read_float(bone_matrix + 0x30 * self.Aimspot + 0x2C)

    def get_view_offset(self):
        self.ViewOffset = self.pm.read_int(self.TargetPlayer + m_vecViewOffset)

def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY

def CalcDistance(current: Vector, new: Vector):
    distance = Vector(0, 0, 0)

    distance.x = new.x - current.x

    if distance.x < -89:
        distance.x += 360
    elif distance.x > 89:
        distance.x -= 360
    if distance.x < 0.0:
        distance.x = -distance.x

    distance.y = new.y - current.y
    if distance.y < - 180:
        distance.y += 360
    elif distance.y > 180:
        distance.y -= 360
    if distance.y < 0.0:
        distance.y = -distance.y

    mag = sqrt(distance.x * distance.x + distance.y * distance.y)
    return mag

class LocalPlayer:
    def __init__(self, pm, client, engine_pointer):
        self.Origin = Vector(0, 0, 0)
        self.ViewOffset = Vector(0, 0, 0)
        self.Health = 0
        self.Team = 0
        self.LocalPlayer = 0
        self.pm = pm
        self.client = client
        self.engine_pointer = engine_pointer
        self.Distance = 0
        self.Pitch = 0
        self.Yaw = 0

    def get(self):
        self.LocalPlayer = self.pm.read_uint(self.client + dwLocalPlayer)

    def get_origin(self):
        self.Origin.x = self.pm.read_float(self.LocalPlayer + m_vecOrigin)
        self.Origin.y = self.pm.read_float(self.LocalPlayer + m_vecOrigin + 4)
        self.Origin.z = self.pm.read_float(self.LocalPlayer + m_vecOrigin + 8) + self.ViewOffset.z

    def get_view_offset(self):
        self.ViewOffset.x = self.pm.read_float(self.engine_pointer + dwClientState_ViewAngles)
        self.ViewOffset.y = self.pm.read_float(self.engine_pointer + dwClientState_ViewAngles + 0x4)
        self.ViewOffset.z = self.pm.read_float(self.LocalPlayer + m_vecViewOffset + 0x8)

    def get_health(self):
        self.Health = self.pm.read_int(self.LocalPlayer + m_iHealth)

    def get_team(self):
        self.Team = self.pm.read_int(self.LocalPlayer + m_iTeamNum)

    def get_distance(self, TargetPlayer):
        delta = Vector(0, 0, 0)
        delta.x = TargetPlayer.x - self.Origin.x
        delta.y = TargetPlayer.y - self.Origin.y
        delta.z = TargetPlayer.z - (self.Origin.z - self.ViewOffset.z)
        distance = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
        distance2 = sqrt(delta.x * delta.x + delta.y * delta.y)
        self.Distance = distance2
        return distance

    def aim_at(self, TargetPlayer, OldDelta, fov):
        delta = Vector(0, 0, 0)
        delta.x = self.Origin.x - TargetPlayer.x
        delta.y = self.Origin.y - TargetPlayer.y
        delta.z = self.Origin.z - TargetPlayer.z
        hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
        pitch = atan(delta.z / hyp) * 180 / pi
        yaw = atan(delta.y / delta.x) * 180 / pi
        if delta.x >= 0.0:
            yaw += 180.0
        pitch, yaw = normalizeAngles(pitch, yaw)
        if -89 <= pitch <= 89 and -180 <= yaw <= 180 and self.Distance:
            if OldDelta.x == TargetPlayer.x and OldDelta.y == TargetPlayer.y:
                return Vector(TargetPlayer.x, TargetPlayer.y, TargetPlayer.z)
            else:
                NewDelta = Vector(TargetPlayer.x, TargetPlayer.y, TargetPlayer.z)
                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles, pitch)
                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
                self.Yaw = yaw
                self.Pitch = pitch
                return NewDelta

