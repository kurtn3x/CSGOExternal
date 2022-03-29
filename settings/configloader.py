import configparser

config = configparser.ConfigParser()
config["AIMBOT"] = {"enabled": 0, "fov": 0, "aimspots": [0, 0, 0, 0, 0], "spotted": 0, "smooth": 0, "smoothvalue": 0}
config["VISUAL"] = {"glow_enabled": 0, "glow_team": 0, "glow_enemy" : 0, "glow_team_color": [0, 0, 0],
                    "glow_enemy_color": [0, 0, 0], "chams_enabled": 0, "chams_team" : 0, "chams_enemy": 0,
                    "chams_team_color" : [0,0,0], "chams_enemy_color" : [0,0,0], "nightmode_enabled" : 0,
                    "nightmodevalue" : 0, "brightmodels_enabled": 0, "brightmodels_value": 0, "fovchanger_enabled" : 0,
                    "fovchanger_value": 0}
config["MISC"] = {"bunnyhop_enabled" : 0, "bunnyhop_autostrafe" : 0, "nohands_enabled" : 0}

with open('example.ini', 'w') as configfile:
    config.write(configfile)
