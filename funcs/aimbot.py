from classes.Vector import Vector
from math import *
from offsets.offsets import *


def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex

    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey

    return distancex, distancey


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


class TargetPlayer:
    def __init__(self, TargetPlayer, aimspot, pm):
        self.pm = pm
        self.TargetPlayer = TargetPlayer
        self.MaxPlayers = 32
        self.Origin = Vector(0, 0, 0)
        self.Health = 0
        self.Team = 0
        self.BonePos = Vector(0, 0, 0)
        self.ViewOffset = Vector(0, 0, 0)
        self.Dormant = 0
        self.SpottedMask = 0
        self.Spotted = 0
        # Head, upper body, lower body, legs, arms
        self.IndexToAimspot = {0: 8, 1: 5, 2: 3, 3: 1, 4: 0}
        self.Aimspots = aimspot # [0, 0, 0, 0, 0]
        self.Aimspot = 0

    def get_dormant(self):
        self.Dormant = self.pm.read_uint(self.TargetPlayer + m_bDormant)

    def get_spotted_mask(self):
        self.SpottedMask = self.pm.read_uint(self.TargetPlayer + m_bSpottedByMask)

    def get_spotted(self):
        self.Spotted = self.pm.read_uint(self.TargetPlayer + m_bSpotted)

    def get_origin(self):
        # doesnt do anything for now
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

    def get_best_bone(self, LocalPlayerOrigin):
        delta = Vector(0, 0, 0)
        best_hyp = 11111
        best_spot = 0
        for index, b in enumerate(self.Aimspots):
            if b == 1:
                # maybe rewrite to b>0 and just input aimspot nr, so the dic isnt needed
                self.Aimspot = self.IndexToAimspot[index]
                self.get_bone_matrix()
                delta.x = LocalPlayerOrigin.x - self.BonePos.x
                delta.y = LocalPlayerOrigin.y - self.BonePos.y
                delta.z = LocalPlayerOrigin.z - self.BonePos.z
                hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
                if hyp < best_hyp:
                    best_hyp = hyp
                    best_spot = self.Aimspot
        self.Aimspot = best_spot


class LocalPlayer:
    def __init__(self, pm, client, engine_pointer, engine):
        self.Origin = Vector(0, 0, 0)
        self.ViewOffset = Vector(0, 0, 0)
        self.Health = 0
        self.Team = 0
        self.LocalPlayer = 0
        self.engine = engine
        self.pm = pm
        self.client = client
        self.engine_pointer = engine_pointer
        self.Distance = 0
        self.Pitch = 0
        self.Yaw = 0
        self.ID = 0
        self.PunchX = 0
        self.PunchY = 0

    def get(self):
        self.LocalPlayer = self.pm.read_uint(self.client + dwLocalPlayer)

    def get_id(self):
        self.ID = self.pm.read_uint(self.engine_pointer + dwClientState_GetLocalPlayer)

    def get_punch(self):
        self.PunchX = self.pm.read_float(self.LocalPlayer + m_aimPunchAngle)
        self.PunchY = self.pm.read_float(self.LocalPlayer + m_aimPunchAngle + 0x4)

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
        self.Distance = distance
        return distance

    def aim_at(self, target_player, old_distance_x, old_distance_y, Spotted, FOV, RCS, Smooth, Smoothvalue):
        self.get_view_offset()
        self.get_origin()
        target_player.get_view_offset()
        target_player.get_spotted()
        target_player.get_spotted_mask()
        target_player.get_best_bone(self.Origin)
        target_player.get_bone_matrix()

        delta = Vector(0, 0, 0)
        delta.x = self.Origin.x - target_player.BonePos.x
        delta.y = self.Origin.y - target_player.BonePos.y
        delta.z = self.Origin.z - target_player.BonePos.z

        hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
        pitch = atan(delta.z / hyp) * 180 / pi
        yaw = atan(delta.y / delta.x) * 180 / pi

        if delta.x >= 0.0:
            yaw += 180.0

        pitch, yaw = normalizeAngles(pitch, yaw)

        distance_x, distance_y = calc_distance(self.ViewOffset.x, self.ViewOffset.y, pitch, yaw)

        if -89 <= pitch <= 89 and -180 <= yaw <= 180:
            if distance_x < FOV and distance_y < FOV:
                if distance_x < old_distance_x and distance_y < old_distance_y:
                    old_distance_x = distance_x
                    old_distance_y = distance_y
                    if RCS and self.pm.read_int(self.LocalPlayer + m_iShotsFired) > 1:
                        if Spotted:
                            self.get_id()
                            if target_player.SpottedMask & (1 << self.ID):
                                self.get_punch()
                                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles,
                                                    pitch - (self.PunchX * 2))
                                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4,
                                                    yaw - (self.PunchY * 2))
                                return old_distance_x, old_distance_y

                        else:
                            self.get_punch()
                            self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles,
                                                pitch - (self.PunchX * 2))
                            self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4,
                                                yaw - (self.PunchY * 2))
                            return old_distance_x, old_distance_y

                    else:
                        if Spotted:
                            if target_player.SpottedMask & (1 << self.ID):
                                self.get_punch()
                                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles,
                                                    pitch - (self.PunchX * 2))
                                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4,
                                                    yaw - (self.PunchY * 2))
                                return old_distance_x, old_distance_y
                        else:
                            self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles, pitch)
                            self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
                            return old_distance_x, old_distance_y

    # delta = Vector(0, 0, 0)
    # delta.x = self.Origin.x - target_player.BonePos.x
    # delta.y = self.Origin.y - target_player.BonePos.y
    # delta.z = self.Origin.z - target_player.BonePos.z
    # hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
    # pitch = atan(delta.z / hyp) * 180 / pi
    # yaw = atan(delta.y / delta.x) * 180 / pi
    #
    # if delta.x >= 0.0:
    #     yaw += 180.0
    # pitch, yaw = normalizeAngles(pitch, yaw)
    # closest_to_crosshair = True
    # if closest_to_crosshair:
    #     distance_x, distance_y = calc_distance(self.ViewOffset.x, self.ViewOffset.y, pitch, yaw)
    #     if distance_x < fov and distance_y < fov:
    #         if -89 <= pitch <= 89 and -180 <= yaw <= 180:
    #             self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles, pitch)
    #             self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
    # else:
    #     currentDistance = self.get_distance(target_player.Origin)
    #     if currentDistance < closestDistance:
    #         closestDistance = currentDistance
    #         if -89 <= pitch <= 89 and -180 <= yaw <= 180 and self.Distance:
    #             if OldDelta.x == target_player.BonePos.x and OldDelta.y == target_player.BonePos.y:
    #                 return closestDistance, Vector(target_player.BonePos.x, target_player.BonePos.y, target_player.BonePos.z)
    #             else:
    #                 distance_x, distance_y = calc_distance(self.ViewOffset.x, self.ViewOffset.y, pitch, yaw)
    #                 if distance_x < fov and distance_y < fov:
    #                     NewDelta = Vector(target_player.BonePos.x, target_player.BonePos.y, target_player.BonePos.z)
    #                     self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles, pitch)
    #                     self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4, yaw)
    #                     self.Yaw = yaw
    #                     self.Pitch = pitch
    #                     return closestDistance, NewDelta
