# class Visuals:
#     def __init__(self):
#         self.GlowEnabled = False
#         self.FovChangerEnabled = False
#
#     def toogle_glow(self):
#         if self.GlowEnabled:
#             self.GlowEnabled = False
#         else:
#             self.GlowEnabled = True

def glow(pm, client, dwGlowObjectManager, dwEntityList, m_iTeamNum, m_iGlowIndex):
    glow_manager = pm.read_int(client + dwGlowObjectManager)
    for i in range(1, 32):
        entity = pm.read_int(client + dwEntityList + i * 0x10)

        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)

            if entity_team_id == 2:  # Terrorist
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))  #
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

            elif entity_team_id == 3:  # Counter-terrorist
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
