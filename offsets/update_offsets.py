import requests
import os

def update_offsets():
    r = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.cs")
    x = r.text
    x = x.split(";")
    i = 0
    path = os.path.join("offsets", "offsets.py")
    f = open(path, "w")
    for line in x:
        if i <=4:
            i+=1
        else:
            line = line.replace("public", "")
            line = line.replace("const", "")
            line = line.replace("Int32", "")
            line = line.replace("{", "")
            line = line.replace("}", "")
            line = line.replace("static class signatures", "")
            line = line.replace("//", "#")
            line = line.strip()
            i += 1
            f.write(line + "\n")
