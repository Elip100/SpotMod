import utils, shutil, os, json

def update():
    if os.path.exists("SpotMod-dat"):
        update__0_4()
    elif not os.path.exists(utils.sm_appdata):
        create_sm_appdata()

def update__0_4():
    shutil.move("SpotMod-dat", utils.datfolder)

    data = json.load(open("data.json"))
    data["version"] = 0.4
    json.dump(data, open("data.json", "w"))

    shutil.move("data.json", utils.maindata)

def create_sm_appdata():
    shutil.copytree(utils.defdat, utils.sm_appdata)