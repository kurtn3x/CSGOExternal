from offsets.offsets import *


def glow(pm, client, glow_manager, myteamid, glow_enemy, glow_team):
    for i in range(1, 32):
        entity = pm.read_int(client + dwEntityList + i * 0x10)
        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)
            entity_dormant = pm.read_int(entity + m_bDormant)
            entity_health = pm.read_int(entity + m_iHealth) / 100

            if entity_dormant:
                continue

            if glow_enemy and entity_team_id != myteamid:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, 1.0 - entity_health)
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, entity_health)
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, 0.0)
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, 0.8)
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)


            if glow_team and entity_team_id == myteamid:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)


def nightmode(pm, client, nightmode_light_value):
    for i in range(0, 2048):
        entity = pm.read_uint(client + dwEntityList + i * 0x10)
        if entity:
            EntityClassID = pm.read_int(entity + 0x8)
            huita1 = pm.read_int(EntityClassID + 2 * 0x4)
            huita2 = pm.read_int(huita1 + 0x1)
            huita3 = pm.read_int(huita2 + 20)

            if True:
                pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                pm.write_float(entity + m_flCustomAutoExposureMin, nightmode_light_value)
                pm.write_float(entity + m_flCustomAutoExposureMax, nightmode_light_value)

