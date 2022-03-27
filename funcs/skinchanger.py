import pymem

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

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)
local_player = pm.read_uint(client + dwLocalPlayer)

for i in range(0, 8):
    currentWeapon = pm.read_int(local_player + m_hMyWeapons + (i - 1) * 0x4) & 0xFFF
    currentWeapon = pm.read_int(client + dwEntityList + (currentWeapon - 1) * 0x10)
    if currentWeapon:
        weapon_id = pm.read_short(currentWeapon + m_iItemDefinitionIndex)
        print(weapon_id)
        if weapon_id == 7:
            while True:
                fallbackPaint = 180
                weapon_owner = pm.read_int(currentWeapon + m_OriginalOwnerXuidLow)
                x = pm.read_int(currentWeapon + m_nFallbackPaintKit)
                print(x)
                pm.write_int(currentWeapon + m_iItemIDHigh, -1)
                pm.write_int(currentWeapon + m_nFallbackPaintKit, fallbackPaint)
                pm.write_float(currentWeapon + m_flFallbackWear, float(0.000001))
                pm.write_int(currentWeapon + m_iAccountID, weapon_owner)
                pm.write_int(currentWeapon + m_nFallbackSeed, 180)
                pm.write_int(currentWeapon + m_nFallbackStatTrak, 1337)