from offsets.offsets import *


def glow(pm, client, glow_manager, myteamid, glow_enemy, glow_team, Color_team, Color_enemy, maxplayers):
    for i in range(0, maxplayers):
        entity = pm.read_int(client + dwEntityList + i * 0x10)
        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)
            entity_dormant = pm.read_int(entity + m_bDormant)
            # entity_health = pm.read_int(entity + m_iHealth) / 100

            if entity_dormant:
                continue

            if glow_enemy and entity_team_id != myteamid:
                # pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, 1.0 - entity_health)
                # pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, entity_health)
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Color_enemy.R / 255.0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Color_enemy.G / 255.0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Color_enemy.B / 255.0))

                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, 1.0)
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)


            if glow_team and entity_team_id == myteamid:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Color_team.R))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Color_team.B))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Color_team.G))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

