from classes.Vector import Vector
from math import *
from offsets.offsets import *
from random import randint


def calc_angle(local: Vector, enemy: Vector):
    delta = Vector(0, 0, 0)
    delta.x = local.x - enemy.x
    delta.y = local.y - enemy.y
    delta.z = local.z - enemy.z

    hyp = sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
    new = Vector(0, 0, 0)
    new.x = asin(delta.z / hyp) * 57.295779513082
    new.y = atan(delta.y / delta.x) * 57.295779513082

    if delta.x >= 0.0:
        new.y += 180.0

    return new


def calc_distance(current: Vector, new: Vector):
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


def get_best_target(pm, client, local_player, target_player, FOV):
    olddist = 111111111
    newdist = 0
    best_target = None
    for i in range(32):
        target_player = pm.read_uint(client + dwEntityList + i * 0x10)
        target_player = TargetPlayer(target_player, pm)

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

        local_player.get_view_offset()
        local_player.get_origin()
        target_player.get_view_offset()
        target_player.get_spotted()
        target_player.get_spotted_mask()
        aimspot = 8
        target_player.get_bone_matrix(aimspot)
        localangle = local_player.ViewOffset
        localpos = local_player.Origin
        entitypos = target_player.BonePos
        new = calc_angle(localpos, entitypos)
        newdist = calc_distance(localangle, new)
        if newdist < olddist and newdist < FOV:
            olddist = newdist
            best_target = target_player
            targetpos = entitypos
            r_localpos = localpos
            r_targetpos = targetpos
    if best_target is not None:
        return best_target, r_localpos, r_targetpos
    else:
        return None, None, None


def normalize_angles(angle: Vector):
    if angle.x > 89:
        angle.x -= 360
    elif angle.x < -89:
        angle.x += 360
    if angle.y > 180:
        angle.y -= 360
    elif angle.y < -180:
        angle.y += 360
    return angle


class TargetPlayer:
    def __init__(self, TargetPlayer, pm):
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

    def get_bone_matrix(self, aimspot):
        # Type 0 = Head, Upp Body, Low Body; 1= Arms; 2= Legs
        # Type 0 is for head
        # Type 1 is for upper - lower body
        # type 2 is for arms
        # type 3 is for legs
        bone_matrix = self.pm.read_int(self.TargetPlayer + m_dwBoneMatrix)
        if aimspot == 8:
            self.BonePos.x = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x0C)
            self.BonePos.y = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x1C)
            self.BonePos.z = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x2C)
        elif aimspot == 6 or aimspot == 4:
            self.BonePos.x = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x0C)
            self.BonePos.y = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x1C)
            self.BonePos.z = self.pm.read_float(bone_matrix + 0x30 * aimspot + 0x2C)

    def get_view_offset(self):
        self.ViewOffset = self.pm.read_int(self.TargetPlayer + m_vecViewOffset)



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
        # Head, upper body, lower body, legs, arms
        self.IndexToAimspot = {0: 8, 1: 6, 2: 4, 3: 2, 4: 0}
        self.Aimspot = 0

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

    def get_crosshair_distance(self, angle_to):
        diff = Vector()
        diff.x = self.ViewOffset.x - angle_to.x
        diff.y = self.ViewOffset.y - angle_to.y
        diff.z = self.ViewOffset.z - angle_to.z
        new_dist = sqrt(diff.x * diff.x + diff.y * diff.y + diff.z * diff.z)

        print(new_dist)

    def aim_at(self, Spotted, FOV, Aimspots, maxClients):
        print(FOV)
        olddist = 111111111
        best_target = None
        r_localpos = None
        best_aimspot = {8: 1111, 6: 1111, 4: 1111, 1: 1111, 3: 1111}
        for i in range(maxClients):
            target_player = self.pm.read_uint(self.client + dwEntityList + i * 0x10)
            target_player = TargetPlayer(target_player, self.pm)

            if not target_player.TargetPlayer:
                continue

            self.get_team()
            target_player.get_team()
            self.get_health()
            target_player.get_health()
            target_player.get_dormant()

            if target_player.Team == self.Team:
                continue
            if target_player.Health < 1 or self.Health < 1:
                continue
            if not self.LocalPlayer:
                continue
            if self.LocalPlayer == target_player.TargetPlayer:
                continue
            if target_player.Dormant:
                continue

            self.get_view_offset()
            self.get_origin()
            target_player.get_view_offset()
            target_player.get_spotted()
            target_player.get_spotted_mask()
            # Spotted
            if Spotted:
                self.get_id()
                if target_player.SpottedMask & (1 << self.ID):
                    for x, f in enumerate(Aimspots):
                        if f == 1:
                            target_player.get_bone_matrix(self.IndexToAimspot[x])
                            localangle = self.ViewOffset
                            localpos = self.Origin
                            entitypos = target_player.BonePos
                            new = calc_angle(localpos, entitypos)
                            newdist = calc_distance(localangle, new)
                            if newdist < olddist and newdist < FOV:
                                aimspot = self.IndexToAimspot[x]
                                olddist = newdist
                                best_target = target_player
                                r_localpos = localpos
                                if best_aimspot[aimspot] > newdist:
                                    best_aimspot[aimspot] = newdist
            else:
                for x, f in enumerate(Aimspots):
                    if f == 1:
                        target_player.get_bone_matrix(self.IndexToAimspot[x])
                        localangle = self.ViewOffset
                        localpos = self.Origin
                        entitypos = target_player.BonePos
                        new = calc_angle(localpos, entitypos)
                        newdist = calc_distance(localangle, new)
                        if newdist < olddist and newdist < FOV:
                            aimspot = self.IndexToAimspot[x]
                            olddist = newdist
                            best_target = target_player
                            r_localpos = localpos
                            if best_aimspot[aimspot] > newdist:
                                best_aimspot[aimspot] = newdist
        if best_target is not None:
            lowest = 11111
            for x in best_aimspot:
                if best_aimspot[x] < lowest:
                    lowest = best_aimspot[x]
                    b_aimspot = x
            best_target.get_bone_matrix(b_aimspot)
            r_targetpos = best_target.BonePos

            unnormal = calc_angle(r_localpos, r_targetpos)
            normal = normalize_angles(unnormal)
            pitch = normal.x
            yaw = normal.y
            if -89 <= pitch <= 89 and -180 <= yaw <= 180:
                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles, pitch)
                self.pm.write_float(self.engine_pointer + dwClientState_ViewAngles + 0x4, yaw)