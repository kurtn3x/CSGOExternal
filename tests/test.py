import pymem

from ctypes import windll, pointer, c_uint32

k32 = windll.kernel32

import re
import requests
import time
import ctypes

radian = 57.295779513082
m_iShotsFired = 0x103E0
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
dwbSendPackets = 0xD9572
dwInput = 0x5220480
m_aimPunchAngle = 0x303C
m_bSpottedByMask = 0x980
m_bSpotted = 0x93D
dwClientState_GetLocalPlayer = 0x180
m_iFOV = 0x31F4
m_iDefaultFOV = 0x333C
dwForceJump = 0x5278DDC
dwForceLeft = 0x31FF378
dwForceRight = 0x31FF384
m_fFlags = 0x104
dwClientState_State = 0x108
m_hMyWeapons = 0x2E08
m_iItemDefinitionIndex = 0x2FBA
m_OriginalOwnerXuidLow = 0x31D0
m_iItemIDHigh = 0x2FD0
m_nFallbackPaintKit = 0x31D8
m_iAccountID = 0x2FD8
m_nFallbackStatTrak = 0x31E4
m_nFallbackSeed = 0x31DC
m_flFallbackWear = 0x31E0
m_bUseCustomAutoExposureMax = 0x9D9
m_bUseCustomAutoExposureMin = 0x9D8
m_flCustomAutoExposureMax = 0x9E0
m_flCustomAutoExposureMin = 0x9DC

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)
local_player = pm.read_uint(client + dwLocalPlayer)
PatternDict = {}


def get_sig(pm, modulename, pattern, extra=0, offset=0,
            relative=True):  # Get_Sig Function that will let us pattern scan for offsets
    if offset == 0:  # very wierd shit happening with the dwbSendPacketsOffset :)
        module = pymem.process.module_from_name(pm.process_handle, modulename)
        bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
        match = re.search(pattern, bytes).start()
        res = match + extra
        return res
    module = pymem.process.module_from_name(pm.process_handle, modulename)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)


def transform_patterns():
    response = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/config.json").json()
    for struct in response["signatures"]:
        old = str(struct["pattern"])
        new = old.replace("?", ".")
        new = new.split(" ")
        newone = ""
        for element in new:
            if element != ".":
                element = r'\x' + element
            newone = newone + element
        PatternDict[struct["name"]] = newone


def getClassID(pm, entity):
    buf = pm.read_int(entity + 8)
    buf = pm.read_int(buf + 2 * 4)
    buf = pm.read_int(buf + 1)
    buf = pm.read_int(buf + 20)
    return


transform_patterns()
while True:
    # 0 no hands
    # 343 CT BLUE
    # 344 CT GREEN
    # 347 BLACK SKINCOLOR
    # 349 CT CAMO
    # 351 CT CAMO2
    # 353 GREY SHIT
    # 355 T LEATHER
    # 358 guy with gold watch
    # 360 CT Blue camo
    # 362 ct green camo
    # 364 some blue jacket
    # 378 also gold watch
    # 381 white jacket
    #
    x = pm.write_int(local_player + 0x258, 381)
    # print(x)

import struct

buf = 1084227584
model_ambient = get_sig(pm, "engine.dll",
                        bytes(PatternDict["model_ambient_min"], encoding="raw_unicode_escape"), 0,
                        4)
model_ambient = int(model_ambient, 0)
# point = pm.read_int(engine + model_ambient - 44)
# xored = buf ^ point
# pm.write_int(engine + model_ambient, xored)

# model_ambient = int(model_ambient, 0)

def f2b(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))


point = pm.read_int(engine + model_ambient - 44)
brightness = 2
addr = 0x12345678
yourval = int(f2b(brightness), 2) ^ addr
pm.write_int(local_player + 0x59003C, yourval)
# while True:
#     for i in range(0, 64):
#         entity = pm.read_uint(client + dwEntityList + i * 0x10)
#         if entity and entity != 0:
#             entityTeam = pm.read_uint(entity + m_iTeamNum)
#             pm.write_uchar(entity + 0x70, 0)
#             pm.write_uchar(entity + 0x71, 255)
#             pm.write_uchar(entity + 0x72, 0)
#             pm.write_uchar(entity + 0x73, 255)



