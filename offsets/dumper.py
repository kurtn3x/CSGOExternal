# https://www.unknowncheats.me/forum/counterstrike-global-offensive/401566-external-netvars-dumper-python.html

import pymem
from netvar_manager import NetvarsManager


def main():
    try:
        csgo_handle = pymem.Pymem('csgo.exe')
    except Exception:
        print('CS:GO process was not found.')
        return
    try:
        print('Dumping the netvars...')
        netvars_manager = NetvarsManager(csgo_handle)
    except Exception:
        import traceback
        print('Error while dumping netvars:')
        traceback.print_exc()
        return
    out_file = input(
        'Enter the out filename (empty string if you want a '
        'dump to be in the terminal): '
    )
    if out_file:
        with open(out_file, 'w+') as fp:
            netvars_manager.dump_netvars(
                fp,
                json_format=out_file.endswith('.json')
            )
    else:
        netvars_manager.dump_netvars()


if __name__ == '__main__':
    main()