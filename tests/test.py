import valvebsp
bsp = valvebsp.Bsp('C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/maps/de_dust2.bsp', )
LUMP_NODES = bsp.__getitem__(5)
LUMP_PLANES = bsp.__getitem__(1)
LUMP_LEAFS =  bsp.__getitem__(10)
for i, x in enumerate(LUMP_LEAFS):
    if "CONTENTS_SOLID" in str(x):
        print("s")