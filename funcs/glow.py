from offsets.offsets import *


def glow(pm, client, glow_manager, myteamid, glow_enemy, glow_team, Color_team, Color_enemy):
    glow_manager = pm.read_int(client + dwGlowObjectManager)
    for i in range(1, 32):
        entity = pm.read_int(client + dwEntityList + i * 0x10)

        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)

            if entity_team_id != myteamid and glow_enemy:  # Terrorist
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Color_enemy.R / 255.0))  # R
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Color_enemy.G / 255.0))  # G
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Color_enemy.B / 255.0))  # B
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enable glow

            elif entity_team_id == myteamid and glow_team:  # Counter-terrorist
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Color_team.R / 255.0))  # R
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Color_team.G / 255.0))  # G
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Color_team.B / 255.0))  # B
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enable glow

